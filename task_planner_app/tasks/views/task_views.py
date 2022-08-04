"""Class and function views for tasks."""
from django.contrib import messages
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.filters import TaskFilter
from tasks.forms import TaskForm, CommentForm
from tasks.models import Task, TaskDependency, TaskList, Comment, Membership
from tasks.utils import UserPermissionMixin
from users.models import User


class TaskCreateView(UserPermissionMixin, LoginRequiredMixin, CreateView):
    """View for creating a task object.

    Inherits:
        UserPermissionMixin: gives access only to group members or higher.
        LoginRequiredMixin: gives site access to signed in users.
        CreateView: gives access to Django pre-built view methods.
    """
    model = TaskList
    form_class = TaskForm
    template_name = 'tasks_template.html'
    
    def get(self, request, pk):
        """Gets the context for template rendering. Defined in get due to potential use with AJAX requests.

        Args:
            request: the HTTP request from frontend.

        Returns:
            Rendered template with context data.
        """
        taskgroup = self.get_object().list_group
        form = TaskForm()
        form.fields['linked_tasks'].queryset = form.fields['linked_tasks'].queryset.filter(list_group=taskgroup)
        tasks = self.get_object().task_set.all()
        myFilter = TaskFilter(self.request.GET, queryset=tasks)
        context = {
            'form': form,
            'members': taskgroup.membership_set.filter(status='Active'),
            'tasklists': taskgroup.tasklist_set.all(),
            'taskgroup': taskgroup,
            'myFilter': myFilter,
            'tasks': myFilter.qs,
            'task_list': self.get_object(),
        }
        return render(request, self.template_name, context)

    def get_success_url(self):
        """Gets the URL if called function is successful."""
        return reverse_lazy('tasks:list_tasks', kwargs={'pk': self.kwargs.get('pk')})
    
    def form_valid(self, form):
        """Creates a task object from the received form.

        Args:
            form: Django form from the frontend.

        Returns:
            Redirection to the success url.
        """
        task_list = self.get_object()
        if super().form_valid(form):
            curr = form.save(commit=False)
            curr.task_list = task_list
            curr.list_group = task_list.list_group
            messages.success(self.request, f'Sucessfully created task {curr.name}')
            curr.save()
            
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context = super().get_context_data(**kwargs)
        taskgroup = self.get_object().list_group
        tasks = self.get_object().task_set.all()
        myFilter = TaskFilter(self.request.GET, queryset=tasks)
        context['members'] = taskgroup.membership_set.filter(status='Active')
        context['tasklists'] = taskgroup.tasklist_set.all()
        context['taskgroup'] = taskgroup
        context['myFilter'] = myFilter
        context['tasks'] = myFilter.qs
        context['task_list'] = self.get_object()
        return context
    

class TaskDetailView(UserPermissionMixin, LoginRequiredMixin, UpdateView):
    """View for displaying the details of a task.

    Inherits:
        UserPermissionMixin: gives access only to group members or higher.
        LoginRequiredMixin: gives site access to signed in users.
        UpdateView: gives access to Django pre-built view methods.
    """
    model = Task
    fields = ['name', 'description', 'deadline', 'status', 'assignee', 'estimation', 'priority', 'linked_tasks']
    template_name = 'task_details.html'

    def get_success_url(self):
        """Gets the URL if called function is successful."""
        return reverse_lazy('tasks:list_tasks', kwargs={'pk': self.get_object().task_list.id})

    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context = super().get_context_data(**kwargs)
        taskgroup = self.get_object().list_group
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        taskform = TaskForm(instance=task)
        taskform.fields['linked_tasks'].queryset = \
        taskform.fields['linked_tasks'].queryset.filter(list_group=taskgroup).exclude(id=pk)
        context['task'] = task
        context['taskgroup'] = taskgroup
        context['members'] = taskgroup.membership_set.filter(status='Active')
        context['tasklists'] = taskgroup.tasklist_set.all()
        context['comments'] = Comment.objects.filter(task=task)
        context['forms'] = {'edit': taskform, 'comment': CommentForm}
        context['recommended'] = recommended(task)
        return context

    def post(self, request, *args, **kwargs):
        """Updates a already created task object from a received form.
        
        Args:
            request: HTTP request from the frontend.

        Returns:
            Redirection to a page displaying the edit form of the specified task.
        """
        task = self.get_object()
        if 'content' in request.POST:
            form = CommentForm(request.POST)
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.task = task
            obj.save()
        else:
            print(request.POST)
            form = TaskForm(request.POST or None, instance=task)
            if form.is_valid():
                curr = form.save(commit=False)
                curr.save()
                if curr.status == 'Complete':
                    workload_list = Task.objects.filter(assignee=curr.assignee).\
                        exclude(status='Complete').values_list('estimation', flat=True)
                    workload_list = [x for x in workload_list if x is not None]
                    workload = sum([int(i) for i in workload_list])
                    curr.assignee.workload = workload
                    curr.assignee.save()
                form.save()
                messages.success(self.request, f'Sucessfully updated task {task.name}')
            else:
                errors = form.errors.get_json_data()
                messages.warning(self.request, errors['__all__'][0]['message']) 
        return redirect(reverse_lazy('tasks:task_details', kwargs={'pk': task.pk}))
    

def recommended(cur_task):
    """Generates a list of users recommended to be assigned to a task based on select criteria.

    Args:
        cur_task: the current task object.

    Returns:
        List of top 3 usernames recommended for the input task.
    """
    cur_tags = cur_task.tags.all()
    taskgroup = cur_task.list_group
    members = Membership.objects.all().filter(group=taskgroup)
    member_priority = {}
    for member in members:
        cur_est_point = cur_task.estimation if cur_task.estimation else 0
        if member.user.capacity > cur_est_point + member.user.workload:
            member_priority[member.user.id] = 0
            proficiencies = member.user.proficiencies.all()
            for tag in cur_tags:
                if tag in proficiencies:
                    member_priority[member.user.id] += 1

    tasks = Task.objects.all().filter(list_group=taskgroup)
    for task in tasks:
        tags = task.tags.all()
        relativeness = 0
        est_point = task.estimation if task.estimation else 0
        if task in cur_task.linked_tasks.all():
            relativeness += 4*est_point
        if task.assignee and task.status == 'Complete':
            for tag in tags:
                if tag in cur_tags:
                    relativeness += est_point
            member_priority[task.assignee.id] += relativeness  
    sorted_keys = sorted(member_priority, key=member_priority.get, reverse=True)
    usernames = []
    for user in sorted_keys[:3]:
        usernames.append(User.objects.get(id=user).username)
    return usernames


class TaskDeleteView(UserPermissionMixin, LoginRequiredMixin, DeleteView):
    """View for ddeleting a task.

    Inherits:
        UserPermissionMixin: gives access only to group members or higher.
        LoginRequiredMixin: gives site access to signed in users.
        DeleteView: gives access to Django pre-built view methods.
    """
    model = Task
    template_name = "task_delete.html"

    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        context['task'] = task
        context['parent'] = TaskDependency.objects.filter(child_task=task)
        context['child'] = TaskDependency.objects.filter(parent_task=task)
        return context

    def get_success_url(self):
        """Gets the URL if called function is successful.
        
        Returns:
            URL to the page for creating a task from within a task list.
        """
        task = self.get_object()
        if task.assignee:
            workload_list = Task.objects.filter(assignee=task.assignee).\
                exclude(status='Complete')
            workload_list = workload_list.exclude(id=task.id)
            workload_list = workload_list.values_list('estimation', flat=True)
            workload_list = [x for x in workload_list if x is not None]
            workload = sum([int(i) for i in workload_list])
            task.assignee.workload = workload
            task.assignee.save()
        return reverse_lazy('tasks:list_tasks', kwargs={'pk': task.task_list.id})