from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.filters import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task, TaskList

from users.models import User

# Create your views here.
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks_template.html'
    
    def get_success_url(self):
        return reverse_lazy("tasks:lists_list", kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_object().task_list.task_set.all()
        taskgroup = self.get_object().task_list.list_group
        myFilter = TaskFilter(self.request.GET, queryset=queryset)
        
        context['task_list_id'] = self.get_object().id 
        context['taskgroup'] = taskgroup
        context['members'] = taskgroup.membership_set.filter(status='Active')
        context['tasks'] = myFilter.qs
        context['myFilter'] = myFilter
        return context
    

class TaskDetailView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'deadline', 'status', 'assignee', 'priority']
    template_name = "task_details.html"
    success_url = reverse_lazy("tasks:tasks")
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context
    
    """def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.name = "Copy of " + obj.name
        obj.pk = None
        obj.save()
        return redirect(self.success_url)"""
        

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_delete.html"
    
    def get_success_url(self):
        return reverse_lazy("tasks:lists_list", kwargs={'pk': self.kwargs.get('pk')})