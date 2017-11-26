from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Photo, Tag

from django.views import generic
from django.utils import timezone


class PhotoView(generic.DetailView):
    model = Photo
    template_name = 'photo/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Photo.objects.filter(taken_at__lte=timezone.now())


@require_http_methods(["GET"])
def tag(request, slug):
    tag_data = Tag.objects.get(tag_slug=slug)
    photo_list = Photo.objects.filter(
        taken_at__lte=timezone.now(),
        tags__tag_slug=slug
    ).order_by('-taken_at')
    paginator = Paginator(photo_list, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        photos = paginator.page(paginator.num_pages)

    return render(request, 'photo/tag.html', {
        'tag': tag_data,
        'photos': photos,
        'paginator': paginator
    })
