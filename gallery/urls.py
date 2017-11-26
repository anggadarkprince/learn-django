from django.conf.urls import url

from . import views

app_name = 'gallery'
urlpatterns = [
    url(r'^photo/(?P<pk>[0-9]+)', views.PhotoView.as_view(), name='photo'),
    url(r'^tag/(?P<slug>[a-zA-Z0-9\-]+)', views.tag, name='tag'),
]
