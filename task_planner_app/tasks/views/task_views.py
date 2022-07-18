from django.contrib import messages
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.filters import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task, TaskList
from tasks.utils import UserPermissionMixin

# Create your views here.
class TaskCreateView(UserPermissionMixin, LoginRequiredMixin, CreateView):
    model = TaskList
    form_class = TaskForm
    template_name = 'tasks_template.html'
    
    def get_success_url(self):
        return reverse_lazy("tasks:lists_list", kwargs={'pk': self.kwargs.get('pk')})
    
    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        task_list = TaskList.objects.get(pk=pk)
        if super().form_valid(form):
            curr = form.save(commit=False)
            curr.task_list = task_list
            curr.list_group = task_list.list_group
            curr.save()
            messages.success(self.request, f'Sucessfully created task {curr.name}')
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taskgroup = self.get_object().list_group
        tasks = self.get_object().task_set.all()
        myFilter = TaskFilter(self.request.GET, queryset=tasks)
        context['taskgroup'] = taskgroup
        context['myFilter'] = myFilter
        context['tasks'] = myFilter.qs
        context['task_list'] = self.get_object()
        return context
    

class TaskDetailView(UserPermissionMixin, LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'deadline', 'status', 'assignee', 'priority']
    template_name = "task_details.html"
    
    def get_success_url(self):
        return reverse_lazy("tasks:lists_list", kwargs={'pk': self.get_object().task_list.id})
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        taskgroup = self.get_object().list_group
        context['tasks'] = Task.objects.all()
        context['taskgroup'] = taskgroup
        context['members'] = taskgroup.membership_set.filter(status='Active')
        return context
    
    """def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.name = "Copy of " + obj.name
        obj.pk = None
        obj.save()
        return redirect(self.success_url)"""
        

class TaskDeleteView(UserPermissionMixin, LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_delete.html"
    
    def get_success_url(self):
        return reverse_lazy("tasks:lists_list", kwargs={'pk': self.get_object().task_list.id})