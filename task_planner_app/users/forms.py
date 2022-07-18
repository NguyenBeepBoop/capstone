from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

from users.models import User


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254)
	class Meta:
		model = User
		fields = ('email', 'username','first_name', 'last_name', 'date_of_birth', 'password1', 'password2', )
    
		widgets = {
        'date_of_birth': forms.DateInput(attrs={'type':'date'})
    	}

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			user = User.objects.exclude(pk=self.instance.pk).get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('"%s" is already in use.' % email)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.exclude(pk=self.instance.pk).get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('"%s" is already in use.' % username)

class UserAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('email', 'password')
	
	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email'].lower()
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Please enter a correct email and password.")

class EditProfileForm(UserChangeForm):
	password = None
	username = forms.CharField(max_length=100)
	
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
			'workload',
			'profile_image',
		]