from rest_api.views import Login, Logout, UserController
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('rest_api.urls')),
    url(r'^api/login/$', Login.as_view(), name='rest_login'),
    url(r'^api/user/$', UserController.as_view(), name='rest_user_details'),
    url('', include('social.apps.django_app.urls'))
]
