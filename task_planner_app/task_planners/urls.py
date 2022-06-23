from atexit import register
from django.urls import path
from . import views
from users.views import register
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', register, name="register"),
]