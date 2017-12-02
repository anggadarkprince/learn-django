from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import When, Case, Count, Sum, IntegerField, Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from gallery.models import Photo
from .models import User
from .forms import RegisterForm, LoginForm, SettingsForm


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            users = User.objects.filter(Q(username=username) | Q(email=username))
            for user in users:
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['avatar'] = user.avatar.__str__()
                    request.session['is_logged_in'] = True
                    return HttpResponseRedirect(reverse('account:photo', args=(user.username,)))

            messages.add_message(request, messages.ERROR, 'Username or password is wrong.')
    else:
        form = RegisterForm()
    return render(request, 'account/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def logout(request):
    try:
        del request.session['user_id']
        del request.session['username']
        del request.session['avatar']
        del request.session['is_logged_in']
        request.session.flush()
    except KeyError:
        pass
    return HttpResponseRedirect('/')


@require_http_methods(["GET", "POST"])
def settings(request):
    user = User.objects.get(username=request.session['username'])
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        form.id = user.id
        form.hashed_password = user.password
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            avatar = form.cleaned_data['avatar']
            about = form.cleaned_data['about']
            new_password = form.cleaned_data['new_password']

            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.about = about
            if avatar is not None:
                user.avatar = avatar
            if new_password is not '':
                user.password = make_password(new_password)
            user.save()

            request.session['username'] = user.username
            request.session['avatar'] = user.avatar.__str__()

            messages.add_message(request, messages.SUCCESS, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse('account:settings'))
    else:
        form = SettingsForm()

    return render(request, 'account/settings.html', {'user': user, 'form': form})


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User()
            user.first_name = username
            user.username = username
            user.email = email
            user.password = make_password(password)
            user.save()

            if user.pk is not None:
                try:
                    send_mail('User registered', 'Please activate your account', 'no-reply@scenary.com', [email], True)
                    message_content = 'We sent you link in <strong>' + email + '</strong> to activate the account.'
                    messages.add_message(request, messages.SUCCESS, mark_safe(message_content))
                    return HttpResponseRedirect(reverse('account:login'))
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            else:
                messages.add_message(request, messages.ERROR, 'Something went wrong.')
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})


def query_user(username):
    album_total = Count('album', distinct=True)
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
    return user


@require_http_methods(["GET"])
def photo(request, username):
    user = query_user(username)
    photos = Photo.objects.filter(album__user__username=username).exclude(status__exact='ARCHIVED').order_by('-taken_at')
    if not username == request.session['username']:
        photos = photos.exclude(status__exact='PRIVATE')
    return render(request, 'account/profile.html', {
        'page': 'photo',
        'template_page': 'gallery/_photo.html',
        'user': user, 'photos': photos
    })


@require_http_methods(["GET"])
def album(request, username):
    user = query_user(username)
    albums = user.album_set.all().order_by('-created_at')
    return render(request, 'account/profile.html', {
        'page': 'album',
        'template_page': 'gallery/_album.html',
        'user': user, 'albums': albums
    })


@require_http_methods(["GET"])
def album_photo(request, username, album_id):
    user = query_user(username)
    album_data = user.album_set.get(id=album_id)
    photos = album_data.photo_set.all()
    return render(request, 'account/profile.html', {
        'page': 'album',
        'template_page': 'gallery/_album_photo.html',
        'user': user, 'album': album_data, 'photos': photos
    })


@require_http_methods(["GET"])
def archive(request, username):
    user = query_user(username)
    archives = Photo.objects.filter(album__user__username=username, status__exact='ARCHIVED')
    return render(request, 'account/profile.html', {
        'page': 'archive',
        'template_page': 'gallery/_archive.html',
        'user': user, 'archives': archives
    })
