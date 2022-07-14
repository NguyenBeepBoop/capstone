from django.contrib import admin
from tasks.models import *
# Register your models here.
admin.site.register(TaskGroup)
admin.site.register(Notification)
admin.site.register(Membership)