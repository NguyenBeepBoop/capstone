"""Class and function views for task groups."""
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import DetailView
from tasks.forms import MembershipForm, NotificationGroupForm
from tasks.models import Membership, Notification, TaskGroup
from tasks.utils import OwnerPermissionMixin, ModeratorPermissionMixin
from users.models import User


class GroupDetailView(OwnerPermissionMixin, LoginRequiredMixin, UpdateView):
    """View for displaying task group details.

    Inherits:
        OwnerPermissionMixin: gives access only to group owners.
        LoginRequiredMixin: gives site access to signed in users.
        UpdateView: gives access to Django pre-built view methods.
    """
    model = TaskGroup
    fields = '__all__'
    template_name = 'group_details.html'
    success_url = reverse_lazy('tasks:dashboard_groups')

    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context= super().get_context_data(**kwargs)
        taskgroup = self.get_object()
        context['tasklists'] = taskgroup.tasklist_set.all()
        context['members'] = taskgroup.membership_set.filter(status='Active')
        return context
        

class GroupDeleteView(OwnerPermissionMixin, LoginRequiredMixin, DeleteView):
    """View to delete a group.

    Inherits:
        OwnerPermissionMixin: gives access only to group owners.
        LoginRequiredMixin: gives site access to signed in users.
        DeleteView: gives access to Django pre-built view methods.
    """
    model = TaskGroup
    template_name = 'group_delete.html'
    success_url = reverse_lazy('tasks:dashboard_groups')


class TaskGroupMembersView(ModeratorPermissionMixin, LoginRequiredMixin, DetailView):
    """View for managing group members and moderator status.

    Inherits:
        ModeratorPermissionMixin: gives access only to group moderators or higher.
        LoginRequiredMixin: gives site access to signed in users.
        DetailView: gives access to Django pre-built view methods.
    """
    model = TaskGroup
    template_name = 'group_membership.html'
    form_class = MembershipForm
    
    def post(self, request, pk, *args, **kwargs):
        """Sends an invitation to a user to join the group as a member.

        Args:
            request: the HTTP request from frontend.
            pk: the primary key of the task group.

        Returns:
            Redirection to manage member's page.
        """
        taskgroup = TaskGroup.objects.get(pk=pk)
        form = MembershipForm(request.POST)
        receiver = User.objects.get(id=request.POST.get('user'))
        desc = request.POST.get('message')
        if form.is_valid():
            membership = Membership.objects.get_or_create(
                user=receiver,
                group=taskgroup,
            )
            
            if not membership[0].role:
                membership[0].role = 'Member'
            membership[0].save()
            
            if membership[0].status == 'Active':
                messages.info(request, f'{receiver} is already a member of this group')
                return redirect(reverse_lazy('tasks:members_list', kwargs={'pk': pk}))
                
            notification = Notification.objects.get_or_create(
                notification_type=3,
                sender=request.user, 
                group=taskgroup, 
                receiver=receiver,
                seen=False
            )
            notification[0].description = desc
            notification[0].seen = False
            notification[0].save()
        return redirect(reverse_lazy('tasks:members_list', kwargs={'pk': pk}))
        
    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context = super().get_context_data(**kwargs)
        taskgroup = self.get_object()
        members = taskgroup.membership_set.filter(status='Active')
        tasklists = taskgroup.tasklist_set.all()
        form = MembershipForm()
        form.fields['user'].queryset = User.objects.exclude(id=self.request.user.id)
        context['taskgroup'] = taskgroup
        context['members'] = members
        context['form'] = form
        context['tasklists'] = tasklists
        return context
        
    def promote(request):
        """Processes the request when a member is promoted to moderator.

        Args:
            request: the HTTP request from frontend.

        Returns:
            A successful HttpResponse.
        """
        if request.is_ajax():
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group_id = request.POST.get('group_id')
            group = TaskGroup.objects.get(id=group_id)
            
            membership = Membership.objects.get(user=user, group=group)
            membership.role = 'Moderator'
            membership.save()
            notification = Notification.objects.get_or_create(
                notification_type = 1,
                sender = request.user,
                receiver = user,
                group = group,
                description = f'@{request.user} has promoted you to Moderator.',
                seen = False
            )

            data = 'success'
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)

    def demote(request):
        """Processes the request when a moderator is demoted to member.

        Args:
            request: the HTTP request from frontend.

        Returns:
            A successful HttpResponse.
        """
        if request.is_ajax():
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group_id = request.POST.get('group_id')
            group = TaskGroup.objects.get(id=group_id)
            
            membership = Membership.objects.get(user=user, group=group)
            membership.role = 'Member'
            membership.save()
            notification = Notification.objects.get_or_create(
                notification_type = 1,
                sender = request.user,
                receiver = user,
                group = group,
                description = f'@{request.user} has demoted you to Member. YIKES!',
                seen = False
            )
            data = 'success'
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)

    def kick(request):
        """Processes the request when a member/moderator is kicked from the group.

        Args:
            request: the HTTP request from frontend.

        Returns:
            A successful HttpResponse.
        """
        if request.is_ajax():
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group_id = request.POST.get('group_id')
            group = TaskGroup.objects.get(id=group_id)
            
            membership = Membership.objects.get(user=user, group=group)
            membership.delete()
            notification = Notification.objects.get_or_create(
                notification_type = 1,
                sender = request.user,
                receiver = user,
                group = group,
                description = f'@{request.user} has kicked you from the group. LATERs',
                seen = False
            )
            data = 'success'
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    
    def leave(request):
        """Processes the request when a member leaves the group.

        Args:
            request: the HTTP request from frontend.

        Returns:
            A successful HttpResponse.
        """
        if request.is_ajax():
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group_id = request.POST.get('group_id')
            group = TaskGroup.objects.get(id=group_id)
            
            membership = Membership.objects.get(user=user, group=group)
            membership.delete()
            data = 'success'
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


class TaskGroupNotifyView(ModeratorPermissionMixin, LoginRequiredMixin, DetailView):
    """View for processing and sending notifications to members in the group.

    Inherits:
        ModeratorPermissionMixin: gives access only to group moderators or higher.
        LoginRequiredMixin: gives site access to signed in users.
        DetailView: gives access to Django pre-built view methods.
    """
    model = TaskGroup
    template_name = 'task_group_notify.html'
    form_class = NotificationGroupForm
    

    def post(self, request, pk, *args, **kwargs):
        """Sends a notification to specified member of the group.

        Args:
            request: the HTTP request from frontend.
            pk: the primary key of the task group.

        Returns:
            Redirection to manage member's page.
        """
        taskgroup = TaskGroup.objects.get(pk=pk)
        member_type = request.POST.get('users')
        if member_type == "Moderators":
            members = taskgroup.membership_set.filter(status='Active', role='Moderator')
        else:
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
                        description=message,
                        seen = False
                    )
                
        return redirect(reverse_lazy('tasks:group_notify', kwargs={'pk': pk}))
    
    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context= super().get_context_data(**kwargs)
        taskgroup = self.get_object()
        members = taskgroup.membership_set.filter(status='Active')
        tasklists = taskgroup.tasklist_set.all()
        context['taskgroup'] =  taskgroup
        context['members'] = members
        context['form'] = self.form_class
        context['tasklists'] = tasklists
        return context
        