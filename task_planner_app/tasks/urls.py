from users.views import LoginView
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from tasks.views import *

app_name='tasks'

urlpatterns = [
    path('tasks/', login_required(TaskCreateView.as_view()), name="tasks"),
    re_path('tasks/(?P<pk>\d+)', login_required(TaskDetailView.as_view()), name="task_details"),
    path('lists/', login_required(TaskListCreateView.as_view()), name='lists'),
    re_path('lists/(?P<pk>\d+)$', login_required(TaskCreateView.as_view()), name="lists_list"),
    path('groups/', login_required(TaskGroupCreateView.as_view()), name='groups'),
    re_path('groups/(?P<pk>\d+)$', TaskListCreateView.as_view(), name="group_list"),
    path('', LoginView, name="home"),

    re_path('tasks_delete/(?P<pk>\d+)', TaskDeleteView.as_view(), name="task_delete"),
    re_path('lists_delete/(?P<pk>\d+)', ListDeleteView.as_view(), name="list_delete"),
    #path('groups_delete/(?P<pk>\d+)', GroupDeleteView.as_view(), name="group_delete"),
]






    
