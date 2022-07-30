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

