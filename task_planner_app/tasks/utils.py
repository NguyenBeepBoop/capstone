from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

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
            messages.info(request, 'You do not have sufficient permissions to view this page')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return super(ViewPermissionsMixin, self).dispatch(
            request, *args, **kwargs)

class UserPermissionMixin(ViewPermissionsMixin):

    def has_permissions(self):
        # here you will have access to both
        # self.get_object() and self.request.user
        queryset = Membership.objects.filter(user=self.request.user, group=self.get_object())
        if queryset.exists():
            return True
        return False
        
class ModeratorPermissionMixin(ViewPermissionsMixin):

    def has_permissions(self):
        # here you will have access to both
        # self.get_object() and self.request.user
        queryset = Membership.objects.filter(user=self.request.user, group=self.get_object(), role='Moderator')
        if queryset.exists():
            return True
        return False
        
class OwnerPermissionMixin(ViewPermissionsMixin):

    def has_permissions(self):
        # here you will have access to both
        # self.get_object() and self.request.user
        return self.request.user == self.get_object().owner