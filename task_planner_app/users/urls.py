from django.conf import settings
from django.urls import path 
from django.conf.urls import url
from . import views 
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    # Miscellaneous URLs for login
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # URLs for resetting the user's password.
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),

    # URLs for viewing user profiles and related functionalities.
    path('profile/', views.ProfileView, name='profile_view'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView, name='profile_view_with_pk'),
    path('profile_edit/', views.EditProfileView, name='edit_profile'),

    # URLs for managing friends, friend requests and related functionalities.
    path('friend_request/', views.send_friend_request, name='friend-request'),
    path('friend_request_accept/<friend_request_id>/', views.accept_friend_request, name='friend-request-accept'),
    path('friend_remove/', views.remove_friend, name='remove-friend'),
    path('friend_request_cancel/', views.cancel_friend_request, name='friend-request-cancel'),
    path('friend_request_decline/<friend_request_id>/', views.decline_friend_request, name='friend-request-decline'),

    # URLs for managing user related notifications.
	path('list/<user_id>', views.friends_list_view, name='list'),
    path('notification/friend_accept/<int:notification_pk>', views.AcceptFriendNotification.as_view(), name='notification_friend_accept'),
    path('notification/friend_decline/<int:notification_pk>', views.DeclineFriendNotification.as_view(), name='notification_friend_decline'),

    # URL for generating PDF reports.
    path('pdf_page/', views.PDFView, name='view_pdf'),
    ]

# Adds static and media files to the url list.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)