from django import forms
from datetime import datetime
from django.utils import timezone
from .models import Notification, Task, TaskList, Tags
from users.models import User

class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
            queryset=Tags.objects.filter(status='Active'),
            widget=forms.CheckboxSelectMultiple,
            required=False)
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'status', 'priority', 'task_list', 'assignee', 'tags']
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
        self.fields['message'].widget.attrs['cols'] = 50
        self.fields['message'].widget.attrs['rows'] = 5
        self.fields['users'].widget.attrs['style'] = 'width:150px;'

class TagForm(forms.ModelForm):
    
    class Meta:
        model = Tags
        fields = '__all__'

class MembershipForm(forms.Form):
    ROLE_CHOICES = [
         ('', '---------'),
        ('Moderators', 'Moderators'),
        ('Members', 'Members'),
    ]
    user = forms.ModelChoiceField(queryset=User.objects.all())
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    message = forms.CharField(max_length=2048, widget=forms.Textarea)
