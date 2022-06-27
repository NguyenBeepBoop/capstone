from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from tasks.views import *

app_name='tasks'

urlpatterns = [
    path('tasks/', login_required(TaskCreateView.as_view()), name="tasks"),
    re_path('tasks/(?P<pk>\d+)', login_required(TaskDetailView.as_view()), name="task_details"),
    path('lists/', login_required(TaskListCreateView.as_view()), name='lists'),
    re_path('lists/(?P<pk>\d+)$', TaskDisplView, name="lists_list"),
    
    path('groups/', login_required(TaskGroupCreateView.as_view()), name='groups'),
    re_path('groups/(?P<pk>\d+)$', TaskListDisplView, name="group_list"),
]





    
