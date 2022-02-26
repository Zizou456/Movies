from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Change Password URL
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='account/password_management/password_change.html'),name='password_change'),
    #Password Change Done
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='account/password_management/password_change_done.html'),name='password_change_done'),
    #Reset Password URL
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_management/password_reset.html'), name='password_reset'),
    #Reset Password Request Sent
    path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='account/password_management/password_reset_done.html'),name='password_reset_done'),
    #Reset Password Form
    path('password_reset/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_management/password_reset_form.html'), name='password_reset_confirm'),
    #Reset Password Done
    path('password_reset/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_management/password_reset_complete.html'), name='password_reset_complete'),
]
