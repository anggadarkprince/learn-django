from django.conf.urls import url

from . import views

app_name = 'account'
urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),
    url(r'^(?P<username>[0-9a-zA-Z._]+)/album/(?P<album_id>[0-9]+)', views.album_photo, name='album_photo'),
    url(r'^(?P<username>[0-9a-zA-Z._]+)/album', views.album, name='album'),
    url(r'^(?P<username>[0-9a-zA-Z._]+)/archive', views.archive, name='archive'),
    url(r'^(?P<username>([a-zA-Z0-9._-]+|(?!media).*)$)', views.photo, name='photo'),
]
