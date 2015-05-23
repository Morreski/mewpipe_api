
from django.conf.urls import url
from controllers import video, tag

urlpatterns = [

    url(r'^videos/$', video.VideoControllerGeneral.as_view()),
    url(r'^videos/(?P<uid>([a-f]|[0-9]){8}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){12})$', video.VideoControllerSpecific.as_view()),
    url(r'^videos/(?P<uid>([a-f]|[0-9]){8}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){12})/share$', video.ShareController.as_view()),
    url(r'^videos/(?P<uid>([a-f]|[0-9]){8}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){12})/upload$', video.UploadVideoController.as_view()),

    url(r'^tags/$', tag.TagGeneral.as_view()),
    url(r'^tags/(?P<uid>([a-f]|[0-9]){8}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){4}-([a-f]|[0-9]){12})$', tag.TagSpecific.as_view())
]
