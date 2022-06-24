from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import View
from users.forms import RegistrationForm, UserAuthenticationForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('task_planners:login')
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"


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
