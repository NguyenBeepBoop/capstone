from django.contrib import admin
from tasks.models import *

# Register Django models to the admin page.
admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(TaskGroup)
admin.site.register(Notification)
admin.site.register(Membership)
admin.site.register(Tags)
