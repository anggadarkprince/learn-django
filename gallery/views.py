from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def album(request, username, album_id):
    return render(request, 'gallery/album.html', {'album': album_id})
