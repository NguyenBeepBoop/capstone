from django.contrib import messages
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.filters import ListFilter
from tasks.forms import TaskListForm

from tasks.models import TaskGroup, TaskList
from tasks.utils import OwnerPermissionMixin, UserPermissionMixin, ModeratorPermissionMixin, user_is_member

class TaskListCreateView(UserPermissionMixin, LoginRequiredMixin, CreateView):
    model = TaskList
    form_class = TaskListForm
    template_name = "task_list_create.html"
    success_url = reverse_lazy("tasks:lists")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        taskgroup=TaskGroup.objects.get(pk=pk)
        queryset = TaskGroup.objects.get(pk=pk).tasklist_set.all()
        context['taskgroup'] = taskgroup
        context['members'] = taskgroup.membership_set.filter(status='Active')
        
        context['task_group_id'] = pk
        myFilter = ListFilter(self.request.GET, queryset=queryset)
        context['myFilter'] = myFilter
        context['task_lists'] = myFilter.qs 
        return context


class ListDetailView(UserPermissionMixin, LoginRequiredMixin, UpdateView):
    model = TaskList
    fields = '__all__'
    template_name = "list_details.html"
    success_url = reverse_lazy("tasks:lists")
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['task_lists'] = TaskList.objects.all()
        return context


class ListDeleteView(UserPermissionMixin, LoginRequiredMixin, DeleteView):
    model = TaskList
    template_name = "list_delete.html"
    success_url = reverse_lazy("tasks:lists")
