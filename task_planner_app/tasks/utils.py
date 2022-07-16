from django.http import HttpResponseRedirect
from django.contrib import messages

from tasks.models import Membership

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
    def has_permissions(self):
        return True 

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            messages.error(request, 'You do not have sufficient permissions to view this page')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super(ViewPermissionsMixin, self).dispatch(
            request, *args, **kwargs)

class UserPermissionMixin(ViewPermissionsMixin):

    def has_permissions(self):
        # here you will have access to both
        # self.get_object() and self.request.user
        if hasattr(self.get_object(), 'owner'):
            queryset = Membership.objects.filter(user=self.request.user, group=self.get_object())
            if queryset.exists():
                return True
        elif hasattr(self.get_object(), 'list_group'):
            queryset = Membership.objects.filter(user=self.request.user, group=self.get_object().list_group)
            if queryset.exists():
                return True
        elif hasattr(self.get_object(), 'task_list'):
            queryset = Membership.objects.filter(user=self.request.user, group=self.get_object().task_list.list_group)
            if queryset.exists():
                return True
        return False
        
class ModeratorPermissionMixin(ViewPermissionsMixin):

    def has_permissions(self):
        # here you will have access to both
        # self.get_object() and self.request.user
        if hasattr(self.get_object(), 'owner'):
            queryset = Membership.objects.filter(user=self.request.user, group=self.get_object(), role='Moderator')
            if queryset.exists():
                return True
        elif hasattr(self.get_object(), 'list_group'):
            queryset = Membership.objects.filter(user=self.request.user, group=self.get_object().list_group, role='Moderator')
            if queryset.exists():
                return True
        elif hasattr(self.get_object(), 'task_list'):
            queryset = Membership.objects.filter(user=self.request.user, group=self.get_object().task_list.list_group, role='Moderator')
            if queryset.exists():
                return True
        return False
        
class OwnerPermissionMixin(ViewPermissionsMixin):

    def has_permissions(self):
        # here you will have access to both
        # self.get_object() and self.request.user
        if hasattr(self.get_object(), 'owner'):
            return self.request.user == self.get_object().owner
        elif hasattr(self.get_object(), 'list_group'):
            return self.request.user == self.get_object().list_group.owner
        elif hasattr(self.get_object(), 'task_list'):
            return self.request.user == self.get_object().task_list.list_group.owner
        return False