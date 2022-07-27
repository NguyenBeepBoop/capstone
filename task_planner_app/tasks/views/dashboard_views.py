import json
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView
from tasks.filters import GroupFilter, TaskFilter
from tasks.models import Membership, Task, TaskGroup
from serpapi import GoogleSearch

class DashboardGroups(LoginRequiredMixin, CreateView):
    model = TaskGroup
    fields = ['name', 'description']
    template_name = "dashboard_taskgroups.html"
    success_url = reverse_lazy("tasks:dashboard_groups")
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        groups = Membership.objects.filter(user=self.request.user, status='Active').values_list('group', flat=True)
        queryset = TaskGroup.objects.filter(id__in=groups)
        group_filter = GroupFilter(self.request.GET, queryset=queryset)
        context['group_filter'] = group_filter
        context['task_groups'] = group_filter.qs
        return context
        
    def form_valid(self, form):
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
    model = TaskGroup
    fields = ['name', 'description']
    template_name = "dashboard.html"
    success_url = reverse_lazy("tasks:dashboard")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Membership.objects.filter(user=self.request.user, status='Active').values_list('group', flat=True)
        tasks = Task.objects.filter(assignee=self.request.user, status__in=['To do', 'In progress'], list_group_id__in=groups).order_by('deadline')
        task_filter = TaskFilter(self.request.GET, queryset=tasks)
        context['tasks'] = task_filter.qs
        context['filter'] = task_filter
        return context
    
    def form_valid(self, form):
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
    if request.is_ajax():
        task_id = request.GET.get('task_id', '')
        task = Task.objects.get(id=task_id)
        tags = [t.name for t in task.tags.all()]
        params = {
            "engine": "google",
            "q": task.name + ' ' + ' '.join(tags),
            "api_key": "74d1eb93c70b7cb02803ff4ad122fb0234446f13f44c9f67ed4012d19518f5d8"
        }
        res = {}
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]
        res['task_id'] = task_id
        res['search_results'] = organic_results
        data = json.dumps(res)

    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)