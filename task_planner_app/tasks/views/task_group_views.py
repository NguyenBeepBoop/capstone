from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from tasks.filters import GroupFilter
from tasks.forms import MembershipForm, NotificationGroupForm

from tasks.models import Membership, Notification, TaskGroup
from tasks.utils import OwnerPermissionMixin, ModeratorPermissionMixin, UserPermissionMixin 
from users.models import User

class TaskGroupCreateView(LoginRequiredMixin, CreateView):
    model = TaskGroup
    fields = ['name', 'description']
    template_name = 'task_group_create.html'    
    success_url = reverse_lazy("tasks:groups")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Membership.objects.filter(user=self.request.user).values_list('group', flat=True)
        queryset = TaskGroup.objects.filter(id__in=groups)
        myFilter = GroupFilter(self.request.GET, queryset=queryset)
        context['myFilter'] = myFilter
        context['task_groups'] = myFilter.qs
        return context

    def form_valid(self, form):
        if super().form_valid(form):
            curr = form.save(commit=False)
            curr.owner = self.request.user
            curr.save()
            Membership.objects.get_or_create(
                user=self.request.user,
                group=curr,
                role='Moderator',
                status='Active'
            )
        return redirect(self.success_url)


class GroupDetailView(OwnerPermissionMixin, LoginRequiredMixin, UpdateView):
    model = TaskGroup
    fields = '__all__'
    template_name = "group_details.html"
    success_url = reverse_lazy("tasks:groups")

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['members'] = TaskGroup.objects.get(pk=pk).members
        return context
        

class GroupDeleteView(OwnerPermissionMixin, LoginRequiredMixin, DeleteView):
    model = TaskGroup
    template_name = "group_delete.html"
    success_url = reverse_lazy("tasks:groups")
        


class TaskGroupMembersView(ModeratorPermissionMixin, LoginRequiredMixin, DetailView):
    model = TaskGroup
    template_name = 'group_membership.html'
    form_class = MembershipForm
        
    def post(self, request, pk, *args, **kwargs):
        taskgroup = TaskGroup.objects.get(pk=pk)
        form = MembershipForm(request.POST)
        receiver = User.objects.get(id=request.POST.get('user'))
        desc = request.POST.get('message')
        if form.is_valid():
            membership = Membership.objects.get_or_create(
                user=receiver,
                group=taskgroup,
            )
            
            if not membership[0].role: membership[0].role = 'Member'
            membership[0].save()
            
            if membership[0].status == 'Active':
                messages.info(request, f'{receiver} is already a member of this group')
                return redirect(reverse_lazy('tasks:members_list', kwargs={'pk': pk}))
                
            notification = Notification.objects.get_or_create(
                notification_type=3,
                sender=request.user, 
                group=taskgroup, 
                receiver=receiver,
            )
            notification[0].description = desc
            notification[0].seen = False
            notification[0].save()
        return redirect(reverse_lazy('tasks:members_list', kwargs={'pk': pk}))
        
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        taskgroup = self.get_object()
        members = taskgroup.membership_set.filter(status='Active')
        context = {
            "taskgroup": taskgroup,
            'members': members,
            'form': self.form_class
        }
        return context

class TaskGroupNotifyView(ModeratorPermissionMixin, LoginRequiredMixin, DetailView):
    model = TaskGroup
    template_name = "task_group_notify.html"
    form_class = NotificationGroupForm
    
    def post(self, request, pk, *args, **kwargs):
        taskgroup = TaskGroup.objects.get(pk=pk)
        members = taskgroup.membership_set.filter(status='Active')
        message = request.POST.get('message')
        if request.method == 'POST':
            form = NotificationGroupForm(request.POST)
            if form.is_valid():
                for member in members:
                    Notification.objects.get_or_create(
                        notification_type=1,
                        sender=request.user, 
                        group=taskgroup, 
                        receiver=member.user,
                        description=message
                    )
                
        return redirect(reverse_lazy('tasks:group_notify', kwargs={'pk': pk}))
        
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        taskgroup = self.get_object()
        members = taskgroup.membership_set.filter(status='Active')
        context = {
            "taskgroup": taskgroup,
            'members': members,
            'form': self.form_class
        }
        return context
        