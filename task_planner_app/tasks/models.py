from django.db import models

# Create your models here.

class Task(models.Model):

    TO_DO = 'S1'
    IN_PROG = 'S2'
    REVIEW = 'S3'
    COMPLETE = 'S4'

    STATUS_CHOICES = [
        (TO_DO, 'To do'),
        (IN_PROG, 'In progress'),
        (REVIEW, 'Review'),
        (COMPLETE, 'Complete')
    ]

    LOWEST = 'P1'
    LOW = 'P2'
    MEDIUM = 'P3'
    HIGH = 'P4'
    HIGHEST = 'P5'

    PRIORITY_CHOICES = [
        (LOWEST, 'Lowest'),
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (HIGHEST, 'Highest')
    ]

    task_name = models.CharField(max_length=100) 
    task_description = models.TextField(max_length=2000, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    task_list = models.ForeignKey("TaskList", on_delete=models.CASCADE, null=True, default='')
    #assignee 
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=TO_DO,
    )

    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default=LOWEST,
    )

    

    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ['status', '-priority', models.F('deadline').asc(nulls_last=True)]

class TaskList(models.Model):
    list_name = models.CharField(max_length=100)

    def __str__(self):
        return self.list_name
