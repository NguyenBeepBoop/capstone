"""Class and function views for task lists."""
from django.contrib import messages
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.filters import ListFilter
from tasks.forms import TaskListForm
from tasks.models import TaskGroup, TaskList
from tasks.utils import UserPermissionMixin


class TaskListCreateView(UserPermissionMixin, LoginRequiredMixin, CreateView):
    """View for creating task lists.

    Inherits:
        UserPermissionMixin: gives access only to group members or higher.
        LoginRequiredMixin: gives site access to signed in users.
        CreateView: gives access to Django pre-built view methods.
    """
    model = TaskGroup
    form_class = TaskListForm
    template_name = 'task_list_create.html'
    
    def get_success_url(self):
        """Gets the URL if called function is successful."""
        return reverse_lazy('tasks:group_list', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        """Creates a task list object from the requested form.

        Args:
            form: the Django formatted form received in the request.

        Returns:
            Redirection to success url.
        """
        pk = self.kwargs.get('pk')
        if super().form_valid(form):
            curr = form.save(commit=False)
            curr.list_group = TaskGroup.objects.get(pk=pk)
            curr.save()
            messages.success(self.request, f'Sucessfully created tasklist {curr.name}')
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        taskgroup = TaskGroup.objects.get(pk=pk)
        queryset = TaskGroup.objects.get(pk=pk).tasklist_set.all()
        context['taskgroup'] = taskgroup
        context['members'] = taskgroup.membership_set.filter(status='Active')
        context['tasklists'] = taskgroup.tasklist_set.all()
        context['task_group_id'] = pk
        myFilter = ListFilter(self.request.GET, queryset=queryset)
        context['myFilter'] = myFilter
        context['task_lists'] = myFilter.qs
        return context


class ListDetailView(UserPermissionMixin, LoginRequiredMixin, UpdateView):
    """View for displaying the details of a task list.

    Inherits:
        UserPermissionMixin: gives access only to group members or higher.
        LoginRequiredMixin: gives site access to signed in users.
        UpdateView: gives access to Django pre-built view methods.
    """
    model = TaskList
    fields = '__all__'
    template_name = 'list_details.html'

    def get_success_url(self):
        """Gets the URL if called function is successful."""
        return reverse_lazy('tasks:group_list', kwargs={'pk': self.get_object().list_group.id})
    
    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context= super().get_context_data(**kwargs)
        tasklist = self.get_object()
        context['task_lists'] = tasklist
        context['tasklists'] = tasklist.list_group.tasklist_set.all()
        context['taskgroup'] = tasklist.list_group
        context['members'] = tasklist.list_group.membership_set.filter(status='Active')
        return context


class ListDeleteView(UserPermissionMixin, LoginRequiredMixin, DeleteView):
    """View for deleting a task list.

    Inherits:
        UserPermissionMixin: gives access only to group members or higher.
        LoginRequiredMixin: gives site access to signed in users.
        DeleteView: gives access to Django pre-built view methods.
    """
    model = TaskList
    template_name = 'list_delete.html'

    def get_success_url(self):
        """Gets the URL if called function is successful."""
        return reverse_lazy('tasks:group_list', kwargs={'pk': self.get_object().list_group.id})
