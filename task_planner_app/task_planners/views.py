from django.shortcuts import render
from .models import Task, TaskList
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy



# Create your views here.
def home(request):
    return render(request, 'base.html', {})

def createTask(request):
    task = Task.objects.all().values()
    context= {'task':task}
    return render(request, 'base.html', context)

class TaskCreateView(CreateView):
    model = Task
    fields = ['task_name', 'task_description', 'deadline', 'status', 'priority']
    template_name = 'base.html'
    success_url = reverse_lazy("task_planners:tasks")

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context

class TaskListCreateView(CreateView):
    model = TaskList
    fields = ['list_name']
    template_name = "base.html"
    success_url = reverse_lazy("task_planners:tasks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.get_object().task_set.all()
        context['context'] = context
        context['task_list'] = TaskList.objects.all()
        return context
