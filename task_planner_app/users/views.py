from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import View
from users.forms import RegistrationForm, UserAuthenticationForm
from .models import User

def RegisterView(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        messages.success(request, "You are already authenticated as " + str(user.email))
        return redirect('task_planners:home')

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
            return redirect('home')
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
        return redirect('task_planners:home')

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email'].lower()
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('task_planners:home')

    else:
        form = UserAuthenticationForm()

    context['form'] = form

    return render(request, "login.html", context)

def UserProfileView(request):
    context = {}
    my_profile = None
    user = request.user
    if user.is_authenticated:
        username = request.user.username

    context['username'] = username

    return render(request, 'profile_view.html', context)