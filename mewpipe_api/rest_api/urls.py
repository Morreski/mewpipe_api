
from django.conf.urls import url
from controllers import video

urlpatterns = [

    url(r'^video/$', video.VideoControllerGeneral.as_view()),
    url(r'video/(?P<uid>([a-f]|[0-9]){8}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){12})$', video.VideoControllerSpecific.as_view())
]
