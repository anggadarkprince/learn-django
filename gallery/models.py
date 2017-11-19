from django.db import models
from account.models import User


class TimestampTable(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Photo(TimestampTable):
    PHOTO_STATUS = (
        ('PRIVATE', 'Private'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_title = models.CharField(max_length=200)
    photo_desc = models.CharField(max_length=500, blank=True)
    source = models.ImageField('Image', width_field=4000, height_field=4000)
    mime_type = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=PHOTO_STATUS, default='PUBLISHED')
    likes = models.PositiveIntegerField()
    taken_at = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Photos'
        indexes = [
            models.Index(fields=['photo_title']),
        ]

    def __str__(self):
        return self.photo_title


class Album(TimestampTable):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=50)
    album_desc = models.CharField(max_length=200)
    photos = models.ManyToManyField(Photo)

    class Meta:
        indexes = [
            models.Index(fields=['album_title']),
        ]

    def __str__(self):
        return self.album_title

