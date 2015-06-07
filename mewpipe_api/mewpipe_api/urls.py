"""mewpipe_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from rest_api.views import FacebookLogin, Login, Logout, UserController, PasswordChange
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('rest_api.urls')),
    #url(r'^api/', include('rest_auth.urls')),
    #url(r'^api/verify-email', VerifyEmail.as_view()),
    url(r'^api/login/$', Login.as_view(), name='rest_login'),
    #url(r'^api/logout/$', Logout.as_view(), name='rest_logout'),
    url(r'^api/user/$', UserController.as_view(), name='rest_user_details'),
    url(r'^api/user/password/$', PasswordChange.as_view(), name='rest_password_change'),
    url(r'^api/facebook/$', FacebookLogin.as_view(), name='fb_login')
]
