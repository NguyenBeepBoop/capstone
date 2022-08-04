"""Class definitions for Django forms related to users/accounts."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from tasks.models import Tags, TaskGroup
from users.models import User


class RegistrationForm(UserCreationForm):
    """Configurable form for creating a new user.

    Inherits:
        UserCreationForm: gives access to Django pre-built form methods for users/accounts.
    """
    email = forms.EmailField(max_length=254)
    
    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name', 'date_of_birth', 'password1', 'password2', )
    
        widgets = {
        'date_of_birth': forms.DateInput(attrs={'type':'date'})
        }

    def clean_email(self):
        """Checks if the inputted email is currently being used by another user.

        Raises:
            ValidationError: if email is already in use.
        """
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('"%s" is already in use.' % email)

    def clean_username(self):
        """Checks if the inputted username is currently being used by another user.

        Raises:
            ValidationError: if username is already in use.
        """
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('"%s" is already in use.' % username)


class UserAuthenticationForm(forms.ModelForm):
    """Configurable form for authenticating a user.

    Inherits:
        forms.ModelForm: gives access to Django pre-built form methods for users/accounts.
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
	
    class Meta:
        model = User
        fields = ('email', 'password')
	
    def clean(self):
        """Raises a ValidationError if the user's email and password is not authenticated."""
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Please enter a correct email and password.')


class EditProfileForm(UserChangeForm):
    """Configurable form for updating a user.

    Inherits:
        UserChangeForm: gives access to Django pre-built form methods for users/accounts.
    """
    password = None
    username = forms.CharField(max_length=100)
    proficiencies = forms.ModelMultipleChoiceField(
            queryset=Tags.objects.filter(status='Active').order_by('name'),
            widget=forms.CheckboxSelectMultiple,
            required=False)
    
    class Meta:
        widgets = {
        'date_of_birth': forms.DateInput(attrs={'type':'date'})
        }
        model = User 
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'date_of_birth',
            'capacity',
            'profile_image',
            'proficiencies',
        ]
		

class PDFForm(forms.Form):
    """Configurable form for generating a PDF report.

    Inherits:
        forms.Form: gives access to Django pre-built generic form methods.
    """
    group = forms.ModelChoiceField(queryset=TaskGroup.objects.all())
    user = forms.ModelChoiceField(queryset=User.objects.all())
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    
    class Meta:
        widgets = {
            'from_date': forms.DateInput(attrs={'type':'date'}),
            'to_date': forms.DateInput(attrs={'type':'date'})
        }
	