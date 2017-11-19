from django.db import models


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
    about = models.TextField(blank=True, help_text='Short story about you')
    status = models.TextField(max_length=20, choices=USER_STATUS, default='PENDING')
    created_at = models.DateTimeField('Join Since', auto_now=True)

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
