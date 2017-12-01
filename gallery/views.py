from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, UpdateView, DeleteView

from account.models import User
from .models import Photo, Tag, Album
from .forms import AlbumForm

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


class AlbumCreate(CreateView):
    model = Album
    template_name = 'album/form.html'
    form_class = AlbumForm

    def form_valid(self, form):
        form.instance.user = User.objects.get(username=self.request.session['username'])
        return super(AlbumCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AlbumCreate, self).get_context_data(**kwargs)
        context['form_title'] = 'Create Album'
        return context


class AlbumEdit(UpdateView):
    model = Album
    template_name = 'album/form.html'
    form_class = AlbumForm

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Update Album'
        return context


class AlbumDelete(DeleteView):
    model = Album
    template_name = 'album/confirm_delete.html'

    def get_success_url(self):
        return reverse('account:album', kwargs={'username': self.request.session['username']})
