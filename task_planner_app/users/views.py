from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.views.generic import View
from .models import User
from users.forms import RegistrationForm, UserAuthenticationForm, EditProfileForm
from django.contrib.auth.decorators import login_required

def RegisterView(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        messages.success(request, "You are already authenticated as " + str(user.email))
        return redirect('tasks:groups')

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('tasks:groups')
        else:
            context['form'] = form

    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'register.html', context)

class LogoutView(SuccessMessageMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


def LoginView(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('tasks:groups')

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email'].lower()
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('tasks:groups')

    else:
        form = UserAuthenticationForm()

    context['form'] = form

    return render(request, "login.html", context)

@login_required
def ProfileView(request):
    context = {'user': request.user}
    return render(request, 'profile_view.html', context)

@login_required
def EditProfileView(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES, instance=request.user)

        if form.is_valid():
            user.profile_image.delete()
            form.save()
            return redirect('profile_view')
        
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'edit_profile.html', context)