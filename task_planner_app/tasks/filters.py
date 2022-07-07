import django_filters
from .models import Task, TaskList

class TaskFilter(django_filters.FilterSet):
    
    class Meta:
        model = Task
        fields = {
            #'id': ['exact'],
            'name': ['icontains'],
            'description': ['icontains'],
            'assignee': ['exact'],
        }
        ordering = []

class ListFilter(django_filters.FilterSet):

    class Meta:
        model = TaskList
        fields = {
            'name': ['icontains'],
        }