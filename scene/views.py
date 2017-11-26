from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.utils import timezone
from gallery.models import Photo


class IndexView(generic.ListView):
    template_name = 'scene/index.html'
    context_object_name = 'photos'

    def get_queryset(self):
        photo_list = Photo.objects.all().filter(
            status='PUBLISHED',
            taken_at__lte=timezone.now()
        ).order_by('-taken_at')
        paginator = Paginator(photo_list, 5)  # Show 5 contacts per page

        page = self.request.GET.get('page')
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            photos = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            photos = paginator.page(paginator.num_pages)

        return photos


@require_http_methods(["GET"])
def agreement(request):
    return render(request, 'scene/agreement.html', {})


@require_http_methods(["GET"])
def privacy(request):
    return render(request, 'scene/privacy.html', {})
