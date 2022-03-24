"""Movies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib.auth import views as auth_views
from mywebsite.views import (home_view)
from account.views import (register_view,login_view,logout_view)

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    #home
    path('', home_view, name='home'),
    #signup
    path('register/', register_view, name="register"),
    #login
    path('login/', login_view, name="login"),
    #logout
    path('logout/', logout_view, name="logout"),
    # Reset Password URL
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='account/password_management/password_reset.html'),
         name='password_reset'),
    # Reset Password Request Sent
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_management/password_reset_done.html'), name='password_reset_done'),
    # Reset Password Form
    path('password_reset/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_management/password_reset_form.html'), name='password_reset_confirm'),
    # Reset Password Done
    path('password_reset/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_management/password_reset_complete.html'), name='password_reset_complete'),
    #Profile
    path('profile/',include('account.urls',namespace='profile')),
    #Movie
    path('Movie/',include('movie.urls',namespace='movie')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
