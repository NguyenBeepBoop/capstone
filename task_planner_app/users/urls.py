from django.conf import settings
from django.urls import path 
from django.conf.urls import url
from . import views 
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.RegisterView, name="register"),
    path('login/', views.LoginView, name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
    path('profile/', views.ProfileView, name='profile_view'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView, name='profile_view_with_pk'),
    path('profile_edit/', views.EditProfileView, name='edit_profile'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)