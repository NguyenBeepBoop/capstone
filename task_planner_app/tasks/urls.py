from users.views import LoginView
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from tasks.views import *

app_name='tasks'

urlpatterns = [
    path('', LoginView, name="home"),

    path('tasks/', login_required(TaskCreateView.as_view()), name="tasks"),
    re_path('tasks/(?P<pk>\d+)', login_required(TaskDetailView.as_view()), name="task_details"),
    re_path('tasks_delete/(?P<pk>\d+)', TaskDeleteView.as_view(), name="task_delete"),
    re_path('tasks?sort=(.*)', TaskCreateView.as_view(), name="task_sort"),

    path('lists/', login_required(TaskListCreateView.as_view()), name='lists'),
    re_path('lists/(?P<pk>\d+)$', login_required(TaskCreateView.as_view()), name="lists_list"),
    re_path('lists_delete/(?P<pk>\d+)', ListDeleteView.as_view(), name="list_delete"),
    re_path('list_details/(?P<pk>\d+)$', ListDetailView.as_view(), name="list_details"),

    path('groups/', login_required(TaskGroupCreateView.as_view()), name='groups'),
    re_path('groups/(?P<pk>\d+)$', TaskListCreateView.as_view(), name="group_list"),
    re_path('groups_delete/(?P<pk>\d+)', GroupDeleteView.as_view(), name="group_delete"),
    re_path('group_details/(?P<pk>\d+)$', GroupDetailView.as_view(), name="group_details"),
    
    re_path('groups_notify/(?P<pk>\d+)$', TaskGroupNotify, name="group_notify"),
    re_path('group_members/(?P<pk>\d+)$', MembersListView, name="members_list"),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification_delete'),
]






    
