from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from tasks.models import Membership, TaskGroup

def user_is_owner(request, group):
    if group.owner == request.user:
        return True
    return False

def user_is_moderator(request, group):
    if Membership.objects.filter(user=request.user, group=group, role='Moderator').exists():
        return True
    return False
    
def user_is_member(request, group):
    if Membership.objects.filter(user=request.user, group=group).exists():
        return True
    return False

class ViewPermissionsMixin(object):
    """Base class for all custom permission mixins to inherit from"""
    def has_permissions(self, role=None):
        # here you will have access to both
        # self.get_object() and self.request.user
        user = self.request.user
        group = self.get_object().list_group
        queryset = Membership.objects.filter(user=user, group=group, status='Active')
        if role:
            queryset = queryset.filter(role=role)

        if queryset.exists():
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            messages.error(request, 'You do not have sufficient permissions to view this page')
            if request.META.get('HTTP_REFERER') != request.path:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect(reverse_lazy('tasks:groups'))
        return super(ViewPermissionsMixin, self).dispatch(
            request, *args, **kwargs)

class UserPermissionMixin(ViewPermissionsMixin):
    def has_permissions(self):
        return super().has_permissions()
        
class ModeratorPermissionMixin(ViewPermissionsMixin):
    def has_permissions(self):
        return super().has_permissions(role='Moderator')
        
class OwnerPermissionMixin(ViewPermissionsMixin):
    def has_permissions(self):
        return self.request.user == self.get_object().list_group.owner