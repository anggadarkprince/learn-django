from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
