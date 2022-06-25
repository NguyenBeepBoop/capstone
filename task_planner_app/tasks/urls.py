from atexit import register
from django.urls import path, re_path
from . import views
from users.views import register

import task_planners
app_name='tasks'
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', register, name="register"),
    path('tasks/', views.TaskCreateView.as_view(), name="tasks"),
    re_path('tasks/(?P<pk>\d+)/', views.TaskListCreateView.as_view(), name="tasks")
]