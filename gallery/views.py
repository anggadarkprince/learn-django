from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Photo
from account.models import User


@require_http_methods(["GET"])
def album(request, username):
    user = User.objects.get(username=username)
    albums = user.album_set.all()
    return render(request, 'gallery/album.html', {'user': user, 'albums':albums})


@require_http_methods(["GET"])
def album_photo(request, username, album_id):
    user = User.objects.get(username=username)
    album_data = user.album_set.get(id=album_id)
    photos = album_data.objects.all()
    return render(request, 'gallery/album_photo.html', {'user': user, 'album': album_data, 'photos': photos})


@require_http_methods(["GET"])
def archive(request, username):
    user = User.objects.get(username=username)
    photos = Photo.objects.filter(album__user__username=username, status='ARCHIVED')
    return render(request, 'gallery/archive.html', {'user': user, 'photos': photos})
