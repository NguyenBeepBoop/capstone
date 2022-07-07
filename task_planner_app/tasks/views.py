from ast import Del, Delete
from django.shortcuts import get_object_or_404, render

from tasks.filters import TaskFilter
from .models import Task, TaskList, TaskGroup
from .forms import TaskForm, TaskListForm
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import is_valid_path, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .filters import ListFilter, TaskFilter

# Create your views here.
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks_template.html'
    success_url = reverse_lazy("tasks:tasks")

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context

class TaskListCreateView(CreateView):
    model = TaskList
    form_class = TaskListForm
    template_name = "task_list_create.html"
    success_url = reverse_lazy("tasks:lists")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['tasks'] = self.get_object().task_set.all()
        context['task_lists'] = TaskList.objects.all()
        return context

@login_required
def TaskListDisplView(request, pk):
    template = "task_list.html"
    taskgroups = TaskGroup.objects.get(pk=pk).tasklist_set.all()
    #groups = list(TaskList.objects.get(pk=pk))
    myFilter = ListFilter(request.GET, queryset=taskgroups)
    taskgroups = myFilter.qs
    
    context = {
        "myFilter": myFilter,
        "tasklists": taskgroups,
    }
    print(context)
    return render(request, template, context)
    
@login_required
def TaskDisplView(request, pk):
    template = "task_list.html"
    tasklists = TaskList.objects.get(pk=pk).task_set.all()
    myFilter = TaskFilter(request.GET, queryset=tasklists)
    tasklists = myFilter.qs
    something = TaskList.objects.get(pk=pk)
    context = {
        "myFilter": myFilter,
        "tasklists": tasklists,
        "something": something,
    }
    return render(request, template, context)

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasklists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = TaskFilter(self.request.GET, queryset=self.get_queryset())
        return context
        
class TaskGroupCreateView(CreateView):
    model = TaskGroup
    fields = '__all__'
    template_name = 'task_group_create.html'    
    success_url = reverse_lazy("tasks:groups")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['tasks'] = self.get_object().task_set.all()
        context['task_groups'] = TaskGroup.objects.all()
        return context

    def form_valid(self, form):
        if super().form_valid(form):
            curr = form.save(commit=False)
            curr.owner = self.request.user
            curr.save()
        return redirect(self.success_url)


# Create your views here.
class TaskDetailView(DetailView):
    model = Task
    fields = ['name', 'description', 'deadline', 'status', 'assignee', 'priority']
    template_name = "task_details.html"
    success_url = reverse_lazy("tasks:tasks")
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context
    
    def post(self, *args, **kwargs):
        obj = self.get_object()
        obj.name = "Copy of " + obj.name
        obj.pk = None
        obj.save()
        return redirect(self.success_url)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = reverse_lazy("tasks:tasks")


class ListDeleteView(DeleteView):
    model = TaskList
    template_name = "list_delete.html"
    success_url = reverse_lazy("tasks:lists")
