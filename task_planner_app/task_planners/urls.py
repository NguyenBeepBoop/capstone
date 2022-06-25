from django.urls import path
from . import views

app_name = 'task_planners'

urlpatterns = [
    path('', views.home, name="home"),
]