from django import forms
from datetime import datetime
from django.utils import timezone
from .models import Task, TaskList

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'status', 'priority', 'task_list', 'assignee']
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'datetime-local'})
        }

class TaskListForm(forms.ModelForm):

    class Meta:
        model = TaskList
        fields = '__all__'
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'datetime-local'})
        }