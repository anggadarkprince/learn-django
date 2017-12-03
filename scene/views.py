from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.utils import timezone
from gallery.models import Photo, Album
from account.models import User


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
def search(request, section):
    query = request.GET['q']
    if section == 'album':
        results = Album.objects.filter(album_title__contains=query)
        template = 'search/_album.html'
    elif section == 'user':
        f_name_condition = Q(first_name__contains=query)
        l_name_condition = Q(last_name__contains=query)
        email_condition = Q(email__contains=query)
        username_condition = Q(username__contains=query)
        results = User.objects.filter(f_name_condition or l_name_condition or email_condition or username_condition)
        template = 'search/_user.html'
    else:
        section = 'photo'
        results = Photo.objects.filter(photo_title__contains=query).filter(status__exact='PUBLISHED')
        template = 'search/_photo.html'

    return render(request, 'search/search.html', {
        'query': query,
        'type_search': section,
        'results': results,
        'search_page': template,
    })


@require_http_methods(["GET"])
def agreement(request):
    return render(request, 'scene/agreement.html', {})


@require_http_methods(["GET"])
def privacy(request):
    return render(request, 'scene/privacy.html', {})
