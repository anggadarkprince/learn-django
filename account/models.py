from django.db import models
from django.db.models import When, Case, Count, Sum, IntegerField


class User(models.Model):
    USER_STATUS = (
        ('PENDING', 'Pending'),
        ('ACTIVATED', 'Activated'),
        ('SUSPENDED', 'Suspended'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    avatar = models.ImageField('Image', upload_to='img/avatars/')
    about = models.TextField(blank=True, help_text='Short story about you')
    status = models.TextField(max_length=20, choices=USER_STATUS, default='PENDING')
    created_at = models.DateTimeField('Join Since', auto_now=True)

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def album_total(self):
        return self.album_set.count()

    def photo_total(self):
        return self.album_set.annotate(num_photos=Count('photo', distinct=True))

    def find(self, username):
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
        user = self.objects.annotate(
            num_albums=album_total, num_all_photos=all_photo_total,
            num_published_photos=published_photo_total, num_private_photos=private_photo_total,
            num_archived_photos=archived_photo_total
        ).get(username=username)
        return user

    class Meta:
        indexes = [
            models.Index(fields=['email', 'username']),
            models.Index(fields=['email'], name='email_idx'),
        ]

    @property
    def full_name(self):
        """Returns the person's full name."""
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return self.first_name
