# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 08:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_remove_photo_mime_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
