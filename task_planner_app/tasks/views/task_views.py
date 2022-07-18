from django.contrib import messages
from braces.views import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.filters import TaskFilter
from tasks.forms import TaskForm, CommentForm
from tasks.models import Task, TaskGroup, TaskList, Comment
from tasks.utils import UserPermissionMixin, user_is_member


from users.models import User

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
            if curr.assignee and curr.estimation:
                user = User.objects.get(id=curr.assignee.id)
                user.workload += curr.estimation
                user.save()
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
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        context['task'] = task
        context['taskgroup'] = taskgroup
        context['members'] = taskgroup.membership_set.filter(status='Active')
        context['comments'] = Comment.objects.filter(task=task)
        context['forms'] = {'edit': TaskForm(instance=task), 'comment': CommentForm}
        return context

    def edit():
        pass

    def comment():
        pass

    def post(self, request, *args, **kwargs):

        if "content" in request.POST:
            form = CommentForm(request.POST)
            obj = form.save(commit=False)
            obj.user = self.request.user
            pk = self.kwargs.get('pk')
            obj.task = Task.objects.get(pk=pk)
            obj.save()
        else:
            pk = self.kwargs.get('pk')
            task = Task.objects.get(pk=pk)
            form = TaskForm(request.POST, instance=task)
            form.save()
        return redirect(reverse_lazy('tasks:lists_list', kwargs={'pk': 1}))
        

class TaskDeleteView(UserPermissionMixin, LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_delete.html"
    
    def get_success_url(self):
        return reverse_lazy("tasks:lists_list", kwargs={'pk': self.get_object().task_list.id})