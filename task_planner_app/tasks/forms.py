from django import forms
from datetime import datetime
from django.utils import timezone
from .models import Task

class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'deadline', 'status', 'priority']
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'datetime-local'})
        }