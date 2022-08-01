from django.forms import ValidationError
from django.utils.functional import cached_property
from django.db import models
from django.conf import settings
from tasks.const import TaskStatus, status_color
#from users.models import FriendRequest
# Create your models here.


STATUS_CHOICES = [
    ('To do', 'To do'),
    ('In progress', 'In progress'),
    ('Review', 'Review'),
    ('Complete', 'Complete')
]

PRIORITY_CHOICES = [
    ('5', 'Lowest'),
    ('4', 'Low'),
    ('3', 'Medium'),
    ('2', 'High'),
    ('1', 'Highest')
]

MEM_STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Pending', 'Pending'),
]

ROLE_CHOICES = [
    ('Moderator', 'Moderator'),
    ('Member', 'Member'),
]

TAGS_CHOICES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
]


class Task(models.Model):
    name = models.CharField(max_length=100)
    linked_tasks = models.ManyToManyField("self", through="TaskDependency", symmetrical = False, blank=True)
    description = models.TextField(max_length=2000, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    estimation = models.PositiveIntegerField(blank=True, null=True)
    task_list = models.ForeignKey("TaskList", on_delete=models.CASCADE, null=True, default='')
    list_group = models.ForeignKey("TaskGroup", on_delete=models.CASCADE, null=True, default='')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True) 
    tags = models.ManyToManyField("Tags")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='To do',
    )

    priority = models.CharField(
        max_length=8,
        choices=PRIORITY_CHOICES,
        default='Lowest',
    )

    def __str__(self):
        return self.name
    
    @cached_property
    def status_display(self):
        _status = {
            'status': TaskStatus(self.status).label,
            'style': status_color[TaskStatus(self.status)]
        }
        return _status
        
    @cached_property
    def priority_display(self):
        _priority = {
            'priority': TaskStatus(self.priority).label,
            'style': status_color[TaskStatus(self.priority)]
        }
        return _priority
        
    def clean(self, *args, **kwargs):
        if self.assignee and self.estimation and self.status != 'Complete':
            workload_list = Task.objects.filter(assignee=self.assignee).\
                exclude(status="Complete").values_list('estimation', flat=True)
            workload_list = [x for x in workload_list if x is not None]
            workload = sum([int(i) for i in workload_list])
            if self.assignee.capacity - (workload + self.estimation) > 0:
                self.assignee.workload = workload + self.estimation 
                self.assignee.save()
            else:
                raise ValidationError (f"{self.assignee} does not have enough capacity.", code='invalid')
        elif self.assignee and not self.estimation:
            raise ValidationError ("please provide a completion estimation when allocating an assignee.", code='invalid')
            
        super().clean(*args, **kwargs)
        
        
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
        
        
    class Meta:
        ordering = ['status', '-priority', models.F('deadline').asc(nulls_last=True)]

class TaskList(models.Model):
    name = models.CharField(max_length=100)
    list_group = models.ForeignKey("TaskGroup", on_delete=models.CASCADE, null=True, default='')
    description = models.TextField(max_length=2000, null=True, blank=True)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class TaskGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
                        on_delete=models.SET_NULL, null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', related_name='groups')
    list_group = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='Member')
    status = models.CharField(max_length=15, choices=MEM_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'group',)
        
    def __str__(self):
        return self.user.username + " " + str(self.group)
    
class Notification(models.Model):
	# 1 Group Notification, 2 = Connection Request, 3 = group invite 
    notification_type = models.IntegerField()
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_to', on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_from', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    #friend_request = models.ForeignKey(FriendRequest, on_delete=models.CASCADE, null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username
	
	
class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    status = models.CharField(max_length=15, choices=TAGS_CHOICES, default='Active')

    def __str__(self):
        return self.name

class TaskDependency(models.Model):
    child_task = models.ForeignKey(Task, related_name="child_task", on_delete=models.CASCADE)
    parent_task = models.ForeignKey(Task, related_name="parent_task", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.parent_task.name + ": " + self.child_task.name
