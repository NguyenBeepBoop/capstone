from django.http import HttpResponse
from django.views import View
from braces.views import LoginRequiredMixin
from tasks.models import Membership, Notification 


class RemoveNotification(LoginRequiredMixin, View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')


class AcceptNotification(LoginRequiredMixin, View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.seen = True
        notification.save()
        membership = Membership.objects.get(group=notification.group, user=notification.receiver)
        print(membership)
        membership.status = 'Active'
        membership.save()

        return HttpResponse('Success', content_type='text/plain')


class DeclineNotification(LoginRequiredMixin, View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        
        notification.seen = True
        notification.save()
        membership = Membership.objects.get(group=notification.group, user=notification.receiver)
        membership.delete()

        return HttpResponse('Success', content_type='text/plain')
        