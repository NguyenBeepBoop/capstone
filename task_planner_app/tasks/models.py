from django.db import models
from django.conf import settings
from django.dispatch import receiver
from pytz import timezone
# Create your models here.


STATUS_CHOICES = [
    ('To do', 'To do'),
    ('In progress', 'In progress'),
    ('Review', 'Review'),
    ('Complete', 'Complete')
]

PRIORITY_CHOICES = [
    ('Lowest', 'Lowest'),
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Highest', 'Highest')
]

MEM_STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Pending', 'Pending'),
]

ROLE_CHOICES = [
    ('Moderator', 'Moderator'),
    ('Member', 'Member'),
]
class Task(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField(max_length=2000, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    task_list = models.ForeignKey("TaskList", on_delete=models.CASCADE, null=True, default='')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True) 
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
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
                        on_delete=models.SET_NULL, null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', related_name='groups')
    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='Member')
    status = models.CharField(max_length=15, choices=MEM_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user + " " + self.group
    
class Notification(models.Model):
	# 1 Group Notification, 2 = Connection Request, 
	notification_type = models.IntegerField()
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_to', on_delete=models.CASCADE, null=True)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_from', on_delete=models.CASCADE, null=True)
	group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	description = models.TextField(max_length=2000, null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)
	