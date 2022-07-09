from django.db import models
from django.conf import settings

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
    def __str__(self):
        return self.name

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s - %s" % (self.post.title, self.last_name)