from django.db import models
from account.models import User


class TimestampTable(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Album(TimestampTable):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=50)
    album_desc = models.CharField(max_length=200)

    def num_photos(self):
        return self.photo_set.count()

    class Meta:
        indexes = [
            models.Index(fields=['album_title']),
        ]

    def __str__(self):
        return self.album_title


class Tag(TimestampTable):
    tag_title = models.CharField(max_length=50)
    tag_slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.tag_title


class Photo(TimestampTable):
    PHOTO_STATUS = (
        ('PRIVATE', 'Private'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    )

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    photo_title = models.CharField(max_length=200)
    photo_desc = models.CharField(max_length=500, blank=True)
    source = models.ImageField('Image', upload_to='img/galleries/%Y/%m/%d/')
    status = models.CharField(max_length=20, choices=PHOTO_STATUS, default='PUBLISHED')
    likes = models.PositiveIntegerField()
    taken_at = models.DateTimeField()
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name_plural = 'Photos'
        indexes = [
            models.Index(fields=['photo_title']),
        ]

    def __str__(self):
        return self.photo_title
