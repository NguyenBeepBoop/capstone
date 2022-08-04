"""Utility functions for friend requests."""
from .models import FriendRequest


def get_friend_request_or_false(sender, receiver):
    """Gets the friend request if it exists.

    Returns:
        FriendRequest object otherwise boolean False.
    """
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False