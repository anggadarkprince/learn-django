"""blogo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from visitor import views as visitor

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^discovery', views.discovery, name='discovery'),
    url(r'^search/(?P<section>[A-Za-z]+)?$', views.search, name='search'),
    url(r'^agreement', views.agreement, name='agreement'),
    url(r'^privacy', views.privacy, name='privacy'),
    url(r'^about', visitor.about, name='about'),
    url(r'^polls/', include('polls.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('account.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

