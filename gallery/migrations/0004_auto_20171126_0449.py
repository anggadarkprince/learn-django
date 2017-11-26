# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20171125_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='source',
            field=models.ImageField(upload_to='img/galleries/%Y/%m/%d/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_slug',
            field=models.SlugField(max_length=200),
        ),
    ]
