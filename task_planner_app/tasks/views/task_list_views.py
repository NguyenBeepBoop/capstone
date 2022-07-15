from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.utils import OwnerPermissionMixin, ModeratorPermissionMixin, UserPermissionMixin 
from tasks.filters import ListFilter
from tasks.forms import TaskListForm

from tasks.models import TaskGroup, TaskList


class TaskListCreateView(LoginRequiredMixin, CreateView):
    model = TaskList
    form_class = TaskListForm
    template_name = "task_list_create.html"
    success_url = reverse_lazy("tasks:lists")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        if pk:
            taskgroup=TaskGroup.objects.get(pk=pk)
            queryset = TaskGroup.objects.get(pk=pk).tasklist_set.all()
            context['taskgroup'] = taskgroup
            context['members'] = taskgroup.membership_set.filter(status='Active')
            viewtype = 1
        else:
            queryset = None
            viewtype = 0
        
        context['task_group_id'] = pk
        myFilter = ListFilter(self.request.GET, queryset=queryset)
        context['myFilter'] = myFilter
        context['task_lists'] = myFilter.qs
        context['type'] = viewtype
        return context

class ListDetailView(LoginRequiredMixin, UpdateView):
    model = TaskList
    fields = '__all__'
    template_name = "list_details.html"
    success_url = reverse_lazy("tasks:lists")
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['task_lists'] = TaskList.objects.all()
        return context


class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskList
    template_name = "list_delete.html"
    success_url = reverse_lazy("tasks:lists")
