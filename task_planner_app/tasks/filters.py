from django.forms import DateInput
import django_filters
from .models import STATUS_CHOICES, PRIORITY_CHOICES, Task, TaskGroup, TaskList

class TaskFilter(django_filters.FilterSet):
    deadline = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}))
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)

    order = django_filters.OrderingFilter(
        label='Sort by',
        fields=(
            ('name', 'Name'),

        )
    )
    class Meta:
        model = Task
        fields = {
            #'id': ['exact'],
            'name': ['icontains'],
            'description': ['icontains'],
            'assignee': ['exact'],
            'deadline': ['date'],
            'status': [],
        }
        

class ListFilter(django_filters.FilterSet):

    class Meta:
        model = TaskList
        fields = {
            'name': ['icontains'],
        }

class GroupFilter(django_filters.FilterSet):
        class Meta:
            model = TaskGroup
            fields = {
                'name': ['icontains'],
            }