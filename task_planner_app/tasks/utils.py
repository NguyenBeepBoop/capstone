"""Utility and Helper functions for user permissions."""
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from tasks.models import Membership


def user_is_owner(request, group):
    """Checks if a user is the group owner."""
    if group.owner == request.user:
        return True
    return False


def user_is_moderator(request, group):
    """Checks if a user is a moderator of a group."""
    if Membership.objects.filter(user=request.user, group=group, role='Moderator').exists():
        return True
    return False
    

def user_is_member(request, group):
    """Checks if a user is a member of the group."""
    if Membership.objects.filter(user=request.user, group=group).exists():
        return True
    return False


class ViewPermissionsMixin(object):
    """Base class for all custom permission mixins to inherit from."""
    
    def has_permissions(self, role=None):
        """Checks if the user has the required permissions to access a feature.

        Args:
            role (default None): the user role to check against.

        Returns:
            Boolean to indicate if the user has permissions. 
        """
        user = self.request.user
        group = self.get_object().list_group
        queryset = Membership.objects.filter(user=user, group=group, status='Active')
        if role:
            queryset = queryset.filter(role=role)

        if queryset.exists():
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        """Redirects the user to the correct view based on if the user has the required
        permissions.

        Args:
            request: the HTTP request from the frontend.

        Returns:
            Redirections to the relevant views.
        """
        if not self.has_permissions():
            messages.error(request, 'You do not have sufficient permissions to view this page')
            if request.META.get('HTTP_REFERER') != request.path:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect(reverse_lazy('tasks:dashboard_groups'))
        return super(ViewPermissionsMixin, self).dispatch(
            request, *args, **kwargs)


class UserPermissionMixin(ViewPermissionsMixin):
    """Class to handle permissions for group members.

    Inherits:
        ViewPermissionsMixin: gives access to permissions checking and dispatch.
    """
    def has_permissions(self):
        return super().has_permissions()


class ModeratorPermissionMixin(ViewPermissionsMixin):
    """Class to handle permissions for group moderators.

    Inherits:
        ViewPermissionsMixin: gives access to permissions checking and dispatch.
    """
    def has_permissions(self):
        return super().has_permissions(role='Moderator')


class OwnerPermissionMixin(ViewPermissionsMixin):
    """Class to handle permissions for group owners.

    Inherits:
        ViewPermissionsMixin: gives access to permissions checking and dispatch.
    """
    def has_permissions(self):
        #Overrides the inherited function as there is a shortcut check for owners.
        return self.request.user == self.get_object().list_group.owner