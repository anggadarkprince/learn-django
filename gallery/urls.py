from django.conf.urls import url
from . import views

app_name = 'gallery'
urlpatterns = [
    url(r'^photo/(?P<pk>[0-9]+)', views.PhotoView.as_view(), name='photo'),
    url(r'^tag/(?P<slug>[a-zA-Z0-9\-]+)', views.tag, name='tag'),
    url(r'^album/create', views.AlbumCreate.as_view(), name='album_create'),
    url(r'^album/(?P<pk>[0-9]+)/edit', views.AlbumEdit.as_view(), name='album_edit'),
    url(r'^album/(?P<pk>[0-9]+)/delete', views.AlbumDelete.as_view(), name='album_delete'),
]
