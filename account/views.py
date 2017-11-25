from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.db.models import When, Case, Count, Min, Sum, Avg, Q, IntegerField
from .models import User
from gallery.models import Photo


@require_http_methods(["GET"])
def login(request):
    return render(request, 'account/login.html', {})


@require_http_methods(["GET"])
def register(request):
    return render(request, 'account/register.html', {})


@require_http_methods(["GET"])
def profile(request, username):
    album_total = Count('album', distinct=True, filter=Q(album__id__gt=2))
    all_photo_total = Count('album__photo', distinct=True)
    published_photo_total = Sum(Case(
        When(album__photo__status='PUBLISHED', then=1),
        default=0, output_field=IntegerField()
    ), distinct=True)
    private_photo_total = Sum(Case(
        When(album__photo__status='PRIVATE', then=1),
        default=0, output_field=IntegerField()
    ), distinct=True)
    archived_photo_total = Sum(Case(
        When(album__photo__status='ARCHIVED', then=1),
        default=0, output_field=IntegerField()
    ))
    user = User.objects.annotate(
        num_albums=album_total, num_all_photos=all_photo_total,
        num_published_photos=published_photo_total, num_private_photos=private_photo_total,
        num_archived_photos=archived_photo_total
    ).get(username=username)

    photos = Photo.objects.filter(album__user__username=username).exclude(status__exact='ARCHIVED')
    return render(request, 'account/profile.html', {'user': user, 'photos': photos})
