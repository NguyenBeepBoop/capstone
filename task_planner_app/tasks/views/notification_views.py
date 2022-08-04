"""Class views for sending and actioning notifications."""
from django.http import HttpResponse
from django.views import View
from braces.views import LoginRequiredMixin
from tasks.models import Membership, Notification 


class RemoveNotification(LoginRequiredMixin, View):
    """View to clear the notification (by pressing the 'X').

    Inherits:
        LoginRequiredMixin: gives site access to signed in users.
        View: generic Django view to access pre-built methods.
    """
    
    def delete(self, request, notification_pk, *args, **kwargs):
        """Marks a notification as seen, removing it from the frontend.

        Args:
            notification_pk: The notification's primary key.

        Returns:
            Successful HttpResponse.
        """
        notification = Notification.objects.get(pk=notification_pk)
        notification.seen = True
        notification.save()
        return HttpResponse('Success', content_type='text/plain')


class AcceptNotification(LoginRequiredMixin, View):
    """View to process notifications if the 'Accept' button is pressed.

    Inherits:
        LoginRequiredMixin: gives site access to signed in users.
        View: generic Django view to access pre-built methods.
    """

    def delete(self, request, notification_pk, *args, **kwargs):
        """Marks a notification as seen and actives the relevant membership object.

        Args:
            notification_pk: The notification's primary key.

        Returns:
            Successful HttpResponse.
        """
        notification = Notification.objects.get(pk=notification_pk)

        notification.seen = True
        notification.save()
        membership = Membership.objects.get(group=notification.group, user=notification.receiver)
        membership.status = 'Active'
        membership.save()

        return HttpResponse('Success', content_type='text/plain')


class DeclineNotification(LoginRequiredMixin, View):
    """View to process notifications if the 'Decline' button is pressed.

    Inherits:
        LoginRequiredMixin: gives site access to signed in users.
        View: generic Django view to access pre-built methods.
    """

    def delete(self, request, notification_pk, *args, **kwargs):
        """Marks a notification as seen and deletes the relevant membership object.

        Args:
            notification_pk: The notification's primary key.

        Returns:
            Successful HttpResponse.
        """
        notification = Notification.objects.get(pk=notification_pk)
        
        notification.seen = True
        notification.save()
        membership = Membership.objects.get(group=notification.group, user=notification.receiver)
        membership.delete()

        return HttpResponse('Success', content_type='text/plain')
        