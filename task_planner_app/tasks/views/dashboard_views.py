"""Class and function views for the dashboard."""
import json
from serpapi import GoogleSearch
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin
from tasks.filters import GroupFilter, TaskFilter
from tasks.models import Membership, Task, TaskGroup


class DashboardGroups(LoginRequiredMixin, CreateView):
    """View to create a new group from the dashboard.

    Inherits:
        LoginRequiredMixin: gives site access to signed in users.
        CreateView: gives access to Django pre-built view methods.
    """
    model = TaskGroup
    fields = ['name', 'description']
    template_name = 'dashboard_taskgroups.html'
    success_url = reverse_lazy('tasks:dashboard_groups')
    
    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context= super().get_context_data(**kwargs)
        groups = Membership.objects.filter(user=self.request.user, status='Active').values_list('group', flat=True)
        queryset = TaskGroup.objects.filter(id__in=groups)
        group_filter = GroupFilter(self.request.GET, queryset=queryset)
        context['group_filter'] = group_filter
        context['task_groups'] = group_filter.qs
        return context
        
    def form_valid(self, form):
        """Creates a task group object from the requested form. Creates membership object between user and group.

        Args:
            form: the Django formatted form received in the request.

        Returns:
            Redirection to group dashboard url.
        """
        if super().form_valid(form):
            curr = form.save(commit=False)
            curr.owner = self.request.user
            curr.list_group = curr
            curr.save()
            Membership.objects.get_or_create(
                user=self.request.user,
                group=curr,
                role='Moderator',
                status='Active'
            )
        return redirect(self.success_url)


class Dashboard(LoginRequiredMixin, CreateView):
    """View for displaying tasks details and integrated support system from the dashboard.
    Creates group from this view as well.

    Inherits:
        LoginRequiredMixin: gives site access to signed in users.
        CreateView: gives access to Django pre-built view methods.
    """
    model = TaskGroup
    fields = ['name', 'description']
    template_name = 'dashboard.html'
    success_url = reverse_lazy('tasks:dashboard')
        
    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        groups = Membership.objects.filter(user=user, status='Active').values_list('group', flat=True)
        tasks = Task.objects.filter(assignee=user, status__in=['To do', 'In progress'], list_group_id__in=groups).order_by('deadline')
        task_filter = TaskFilter(self.request.GET, queryset=tasks)
        context['filter'] = task_filter
        context['tasks'] = task_filter.qs
        return context
    
    def form_valid(self, form):
        """Creates a task group object from the requested form. Creates membership object between user and group.

        Args:
            form: the Django formatted form received in the request.

        Returns:
            Redirection to dashboard url.
        """
        if super().form_valid(form):
            curr = form.save(commit=False)
            curr.owner = self.request.user
            curr.list_group = curr
            curr.save()
            Membership.objects.get_or_create(
                user=self.request.user,
                group=curr,
                role='Moderator',
                status='Active'
            )
        return redirect(self.success_url)


@cache_page(60 * 15)
def get_help(request):
    """Sends a Google search request to SerpAPI.

    Args:
        request: data from HTTP request.

    Returns:
        HttpResponse with the API search data.
    """
    if request.is_ajax():
        task_id = request.GET.get('task_id', '')
        task = Task.objects.get(id=task_id)
        tags = [t.name for t in task.tags.all()]
        params = {
            'engine': 'google',
            'q': task.name + ' ' + ' '.join(tags),
            'api_key': '74d1eb93c70b7cb02803ff4ad122fb0234446f13f44c9f67ed4012d19518f5d8'
        }
        search = GoogleSearch(params)
        res = {
            'task_id': task_id,
            'search_results': search.get_dict()['organic_results'],
        }
        data = json.dumps(res)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
