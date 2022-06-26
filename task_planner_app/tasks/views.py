from django.shortcuts import render
from .models import Task, TaskList
from .forms import TaskForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy



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
    fields = ['list_name']
    template_name = "lists_template.html"
    success_url = reverse_lazy("tasks:lists")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['tasks'] = self.get_object().task_set.all()
        context['task_lists'] = TaskList.objects.all()
        return context

# Create your views here.
