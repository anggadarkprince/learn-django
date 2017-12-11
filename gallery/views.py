from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, UpdateView, DeleteView

from account.models import User
from .models import Photo, Tag, Album
from .forms import AlbumForm, AlbumPhotoForm

from django.views import generic
from django.utils import timezone


class PhotoView(generic.DetailView):
    model = Photo
    template_name = 'photo/detail.html'


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


class AlbumPhotoCreate(CreateView):
    model = Photo
    template_name = 'photo/form.html'
    form_class = AlbumPhotoForm

    def form_valid(self, form):
        form.instance.album = Album.objects.get(id=self.kwargs['pk'])
        return super(AlbumPhotoCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AlbumPhotoCreate, self).get_context_data(**kwargs)
        context['form_title'] = 'Upload Photo Album'
        context['album'] = Album.objects.get(id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('account:album_photo', kwargs={
            'username': self.request.session['username'],
            'album_id': self.kwargs['pk']
        })


class PhotoCreate(CreateView):
    model = Photo
    template_name = 'photo/form.html'
    form_class = AlbumPhotoForm

    def form_valid(self, form):
        # form.instance.album = Album.objects.get(id=self.request.POST['album_id'])
        # article = form.save(commit=False)
        # article.album = Album.objects.get(id=self.request.POST['album_id'])

        photo = Photo()
        photo.album = Album.objects.get(id=self.request.POST['album_id'])
        photo.photo_title = form.cleaned_data['photo_title']
        photo.photo_desc = form.cleaned_data['photo_desc']
        photo.source = form.cleaned_data['source']
        photo.status = form.cleaned_data['status']
        photo.taken_at = form.cleaned_data['taken_at']
        photo.save()

        tag_list = form.cleaned_data['tag_list'].split(',')
        for tag_title in tag_list:
            tag_slug = slugify(tag_title)
            available_tag = Tag.objects.filter(tag_slug__exact=tag_slug)
            if available_tag.count() > 0:
                photo.tags.add(available_tag.first())
            else:
                new_tag = Tag.objects.create(tag_title=tag_title, tag_slug=tag_slug)
                photo.tags.add(new_tag)

        return super(PhotoCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PhotoCreate, self).get_context_data(**kwargs)
        context['form_title'] = 'Upload Photo'
        context['albums'] = User.objects.get(username=self.request.session['username']).album_set.all()
        return context

    def get_success_url(self):
        return reverse('account:photo', kwargs={
            'username': self.request.session['username']
        })


class AlbumEdit(UpdateView):
    model = Album
    template_name = 'album/form.html'
    form_class = AlbumForm

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Update Album'
        return context


class AlbumPhotoEdit(UpdateView):
    model = Photo
    template_name = 'photo/form.html'
    form_class = AlbumPhotoForm

    def get_object(self, queryset=None):
        return Photo.objects.get(pk=self.kwargs['pk_photo'])

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Update Photo Album'
        context['album'] = Album.objects.get(id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('gallery:photo', kwargs={
            'pk': self.kwargs['pk_photo']
        })


class PhotoEdit(UpdateView):
    model = Photo
    template_name = 'photo/form.html'
    form_class = AlbumPhotoForm

    def form_valid(self, form):
        form.instance.album = Album.objects.get(id=self.request.POST['album_id'])
        return super(PhotoEdit, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Update Photo'
        context['albums'] = User.objects.get(username=self.request.session['username']).album_set.all()
        return context

    def get_success_url(self):
        return reverse('gallery:photo', kwargs={
            'pk': self.kwargs['pk']
        })


class AlbumDelete(DeleteView):
    model = Album
    template_name = 'album/confirm_delete.html'

    def get_success_url(self):
        return reverse('account:album', kwargs={
            'username': self.request.session['username']
        })


class PhotoDelete(DeleteView):
    model = Photo
    template_name = 'photo/confirm_delete.html'

    def get_success_url(self):
        return reverse('account:photo', kwargs={
            'username': self.request.session['username']
        })


@require_http_methods(["POST"])
def archive(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    photo.status = 'ARCHIVED'
    try:
        photo.save()
        messages.add_message(request, messages.SUCCESS, 'Photo ' + photo.photo_title + ' successfully archived')
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Something went wrong while archiving photo.')
    return HttpResponseRedirect(reverse('account:archive', args=(photo.album.user.username,)))


@require_http_methods(["POST"])
def like(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    photo.likes = photo.likes + 1
    try:
        photo.save()
        return JsonResponse({'status': 'success'})
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Something went wrong'})
