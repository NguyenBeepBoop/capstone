from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Notification, Task, TaskList, TaskGroup
from .forms import TaskForm, TaskListForm
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

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
    tasklists = TaskGroup.objects.get(pk=pk).tasklist_set.all()
    context = {
        "tasklists": tasklists
    }
    return render(request, template, context)
    
@login_required
def MembersListView(request, pk):
    template = "task_list.html"
    tasklists = TaskGroup.objects.get(pk=pk).tasklist_set.all()
    context = {
        "tasklists": tasklists
    }
    return render(request, template, context)
    
@login_required
def TaskDisplView(request, pk):
    template = "task_list.html"
    tasklists = TaskList.objects.get(pk=pk).task_set.all()
    context = {
        "tasklists": tasklists
    }
    return render(request, template, context)

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
        
class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')