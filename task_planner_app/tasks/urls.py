from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required

app_name='tasks'

urlpatterns = [
    path('tasks/', login_required(views.TaskCreateView.as_view()), name="tasks"),
    re_path('tasks/(?P<pk>\d+)/', login_required(views.TaskListCreateView.as_view()), name="tasks")
]