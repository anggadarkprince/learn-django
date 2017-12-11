from django import forms
from django.utils.dateparse import parse_date
from django.utils.datetime_safe import date

from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('user',)


class AlbumPhotoForm(forms.ModelForm):
    album_id = forms.NumberInput()
    tag_list = forms.CharField(max_length=150)
    labels = {
        'source': 'Photo source',
    }

    class Meta:
        model = Photo
        exclude = ('album', 'likes', 'tags')
