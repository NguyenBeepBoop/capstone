from django.contrib import messages
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.filters import ListFilter
from tasks.forms import TaskListForm

from tasks.models import TaskGroup, TaskList
from tasks.utils import OwnerPermissionMixin, UserPermissionMixin, ModeratorPermissionMixin, user_is_member

class TaskListCreateView(LoginRequiredMixin, CreateView):
    model = TaskList
    form_class = TaskListForm
    template_name = "task_list_create.html"
        
    def get_success_url(self):
        return reverse_lazy("tasks:group_list", kwargs={'pk': self.kwargs.get('pk')})
    
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            taskgroup=TaskGroup.objects.get(pk=pk)
            if not (user_is_member(request, taskgroup)):
                messages.error(request, 'You must be a member of this group to access this page.')
                return redirect(reverse_lazy('tasks:groups'))
        return super(TaskListCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        if super().form_valid(form):
            curr = form.save(commit=False)
            curr.list_group = TaskGroup.objects.get(pk=pk)
            curr.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        taskgroup = TaskGroup.objects.get(pk=pk)
        queryset = TaskGroup.objects.get(pk=pk).tasklist_set.all()
        context['taskgroup'] = taskgroup
        context['members'] = taskgroup.membership_set.filter(status='Active')
        viewtype = 1

        context['task_group_id'] = pk
        myFilter = ListFilter(self.request.GET, queryset=queryset)
        context['myFilter'] = myFilter
        context['task_lists'] = myFilter.qs
        context['type'] = viewtype  
        return context


class ListDetailView(UserPermissionMixin, LoginRequiredMixin, UpdateView):
    model = TaskList
    fields = '__all__'
    template_name = "list_details.html"

    def get_success_url(self):
        return reverse_lazy("tasks:group_list", kwargs={'pk': self.get_object().list_group.id})
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['task_lists'] = TaskList.objects.all()
        return context


class ListDeleteView(UserPermissionMixin, LoginRequiredMixin, DeleteView):
    model = TaskList
    template_name = "list_delete.html"

    def get_success_url(self):
        return reverse_lazy("tasks:group_list", kwargs={'pk': self.get_object().list_group.id})
