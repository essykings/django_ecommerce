from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.register, name = 'register'),
    path('login', views.UserLoginView.as_view(), name = 'login'),
    path('logout', views.logout_user, name = 'logout'), #new

   path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'users/password-reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password-reset-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password-reset-confirm.html'), name='password_reset_confirm'),
  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password-reset-complete.html'), name='password_reset_complete'),
]