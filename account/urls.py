from django.urls import path


from account.views import profile_view,profile_settings_view,Custom_Password_Change
from django.contrib.auth import views as auth_views
app_name = 'profile'

urlpatterns = [
    #Profile
    path('',profile_view,name='view'),
    path('edit',profile_settings_view,name='edit'),
    # Password Change
    path('password/',
         Custom_Password_Change.as_view(template_name='account/password_management/password_change.html'),
         name='password_change'),
    # Password Change Done
    path('password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/password_management/password_change_done.html'), name='password_change_done'),
]