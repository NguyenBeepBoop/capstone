"""Class definitions for various Django forms related to tasks i.e. not users/accounts."""
from django import forms
from users.models import User
from .models import Comment, Task, TaskList, Tags


class TaskForm(forms.ModelForm):
    """Configurble form for creating/updating tasks.

    Inherits:
        forms.ModelForm: gives access to Django pre-built form methods.
    """
    tags = forms.ModelMultipleChoiceField(
            queryset=Tags.objects.filter(status='Active').order_by('name'),
            widget=forms.CheckboxSelectMultiple,
            required=False)
            
    linked_tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'estimation', 'assignee', 'status', 'priority', 'tags', 'linked_tasks']
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'datetime-local'})
        }


class TaskListForm(forms.ModelForm):
    """Configurble form for creating/updating task lists.

    Inherits:
        forms.ModelForm: gives access to Django pre-built form methods.
    """

    class Meta:
        model = TaskList
        fields = ['name', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'datetime-local'})
        }

 
class NotificationGroupForm(forms.Form):
    """Configurble form for creating/updating notifications.

    Inherits:
        forms.Form: gives access to Django pre-built form methods.
    """
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
    """Configurble form for creating tags.

    Inherits:
        forms.ModelForm: gives access to Django pre-built form methods.
    """

    class Meta:
        model = Tags
        fields = '__all__'


class MembershipForm(forms.Form):
    """Configurble form for creating/updating user-group memberships.

    Inherits:
        forms.Form: gives access to Django pre-built form methods.
    """
    user = forms.ModelChoiceField(queryset=User.objects.all())
    message = forms.CharField(max_length=2048, widget=forms.Textarea, required=False)
    
    class Meta:
        fields = ['user', 'message']
    
    def __init__(self, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs) 


class CommentForm(forms.ModelForm):
    """Configurble form for creating task comments.

    Inherits:
        forms.ModelForm: gives access to Django pre-built form methods.
    """
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows':'4',
    }))

    class Meta:
        model = Comment 
        fields = ['content']