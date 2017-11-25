from django.conf.urls import url

from . import views
import gallery.views as gallery

app_name = 'account'
urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^register', views.register, name='register'),
    url(r'^(?P<username>[0-9a-zA-Z._]+)/album/(?P<album_id>[0-9]+)', gallery.album, name='album'),
    url(r'^(?P<username>([a-zA-Z0-9._-]+|(?!media).*)$)', views.profile, name='profile'),
]
