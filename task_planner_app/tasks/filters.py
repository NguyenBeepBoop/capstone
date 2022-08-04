"""Classes to configure object filters by properties."""
from django.forms import DateInput
from django_filters import FilterSet, DateFilter, ChoiceFilter, OrderingFilter
from .models import STATUS_CHOICES, Task, TaskGroup, TaskList


class TaskFilter(FilterSet):
    """Filter class for tasks by related properties.
    
    Inherits:
        FilterSet: gives access to Django pre-built filter methods.
    """
    deadline = DateFilter(widget=DateInput(attrs={'type': 'date'}))
    status = ChoiceFilter(choices=STATUS_CHOICES)
    order = OrderingFilter(
        label='Sort by',
        fields=(
            ('id', 'id'),
            ('name', 'name'),
            ('deadline', 'deadline'),
            ('priority', 'priority'),
            ('date_created', 'date_created')

        ),
        field_labels={
            'id': 'ID',
        }
    
    )
    class Meta:
        model = Task
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'assignee': ['exact'],
            'deadline': ['date'],
            'status': [],
        }
        

class ListFilter(FilterSet):
    """Filter class for task lists by related properties.
    
    Inherits:
        FilterSet: gives access to Django pre-built filter methods.
    """
    class Meta:
        model = TaskList
        fields = {
            'name': ['icontains'],
        }


class GroupFilter(FilterSet):
    """Filter class for task groups by related properties.
    
    Inherits:
        FilterSet: gives access to Django pre-built filter methods.
    """
    class Meta:
        model = TaskGroup
        fields = {
            'name': ['icontains'],
        }