from atexit import register
from django.urls import path
from . import views
from users.views import register

import task_planners
app_name='task_planners'
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', register, name="register"),
    path('tasks/', views.TaskCreateView.as_view(), name="tasks"),
    #path('tasks/(?P<pk>\d+)/', views.TaskListCreateView.as_view(), name="tasks")
]