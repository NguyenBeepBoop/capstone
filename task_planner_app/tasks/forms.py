from django import forms
from datetime import datetime
from django.utils import timezone

from users.models import User
from .models import ROLE_CHOICES, Notification, Task, TaskList, Membership


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'status', 'priority', 'assignee']
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'datetime-local'})
        }

class TaskListForm(forms.ModelForm):

    class Meta:
        model = TaskList
        fields = ['name', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'datetime-local'})
        }
        
class NotificationGroupForm(forms.Form):
    ROLE_CHOICES = [
         ('', '---------'),
        ('Moderators', 'Moderators'),
        ('Members', 'Members'),
    ]
    users = forms.ChoiceField(choices=ROLE_CHOICES)
    message = forms.CharField(max_length=2048, widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super(NotificationGroupForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['message'].widget.attrs['cols'] = 10
        self.fields['message'].widget.attrs['rows'] = 10
        self.fields['users'].widget.attrs['style'] = 'width:150px;'


class MembershipForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    message = forms.CharField(max_length=2048, widget=forms.Textarea)