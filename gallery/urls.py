from django.conf.urls import url
from . import views

app_name = 'gallery'
urlpatterns = [
    url(r'^photo/create', views.PhotoCreate.as_view(), name='photo_create'),
    url(r'^photo/(?P<photo_id>[0-9]+)/archive', views.archive, name='photo_archive'),
    url(r'^photo/(?P<pk>[0-9]+)/edit', views.PhotoEdit.as_view(), name='photo_edit'),
    url(r'^photo/(?P<pk>[0-9]+)/delete', views.PhotoDelete.as_view(), name='photo_delete'),
    url(r'^photo/(?P<pk>[0-9]+)', views.PhotoView.as_view(), name='photo'),
    url(r'^tag/(?P<slug>[a-zA-Z0-9\-]+)', views.tag, name='tag'),
    url(r'^album/create', views.AlbumCreate.as_view(), name='album_create'),
    url(r'^album/(?P<pk>[0-9]+)/photo/create', views.AlbumPhotoCreate.as_view(), name='album_photo_create'),
    url(r'^album/(?P<pk>[0-9]+)/edit', views.AlbumEdit.as_view(), name='album_edit'),
    url(r'^album/(?P<pk>[0-9]+)/photo/(?P<pk_photo>[0-9]+)/edit', views.AlbumPhotoEdit.as_view(), name='album_photo_edit'),
    url(r'^album/(?P<pk>[0-9]+)/delete', views.AlbumDelete.as_view(), name='album_delete'),
]
