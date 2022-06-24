from atexit import register
from django.urls import path
from . import views
from users.views import LoginView, RegisterView, LogoutView

app_name = "task_planners"

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]