from django.shortcuts import get_object_or_404, render
from .models import Task, TaskList, TaskGroup
from .forms import TaskForm, TaskListForm
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import is_valid_path, reverse_lazy
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


# Create your views here.
class TaskDetailView(DetailView):
    model = Task
    fields = ['name', 'description', 'deadline', 'status', 'assignee', 'priority']
    template_name = "task_details.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context

'''    def task_copy(request, id):
    new_task = get_object_or_404(Task, pk = id)
    new_task.pk = None
    new_task.name = "Copy of" + new_task.name

    form = TaskForm(request.POST or None, instance = new_task)

    context = {
        "form": form
    }
    return render(request, "tasks_template.html", context)


    class TaskDetailView(DetailView):
    model = Task
    fields = ['name', 'description', 'deadline', 'status', 'assignee', 'priority']
    template_name = "task_details.html"
    success_url = reverse_lazy("tasks:tasks")
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context

    def post(self, request, pk):
        old_task = Task.objects.get(id=pk)
        new_task = Task(name="Copy of" + old_task.name, 
        description=old_task.description, 
        deadline=old_task.deadline, 
        status=old_task.status, 
        priority=old_task.priority, 
        TaskList=old_task.task_list, 
        assignee=old_task.assignee)
        new_task.save()

        return redirect(self.success_url)'''