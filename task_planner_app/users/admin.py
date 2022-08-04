"""Registers user models to Django admin page."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, FriendList, FriendRequest


class UserAdmin(UserAdmin):
    """Register user model."""
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(User, UserAdmin)


class FriendListAdmin(admin.ModelAdmin):
    """Register friend list model."""
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user',]

    class Meta:
        model = FriendList

admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    """Register friend request model."""
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver',]
    search_fields = ['sender__username', 'receiver__username']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)