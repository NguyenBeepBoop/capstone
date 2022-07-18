from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from tasks.filters import GroupFilter, TaskFilter
from tasks.models import Membership, Task, TaskGroup

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
        tasks = Task.objects.filter(assignee=self.request.user, status__in=['To do', 'In progress']).order_by('deadline')
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