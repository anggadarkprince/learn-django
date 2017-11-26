# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('album_title', models.CharField(max_length=50)),
                ('album_desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('photo_title', models.CharField(max_length=200)),
                ('photo_desc', models.CharField(blank=True, max_length=500)),
                ('source', models.ImageField(height_field=4000, upload_to='', verbose_name='Image', width_field=4000)),
                ('mime_type', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('PRIVATE', 'Private'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Archived')], default='PUBLISHED', max_length=20)),
                ('likes', models.PositiveIntegerField()),
                ('taken_at', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User')),
            ],
            options={
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(to='gallery.Photo'),
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User'),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=models.Index(fields=['photo_title'], name='gallery_pho_photo_t_3568c5_idx'),
        ),
        migrations.AddIndex(
            model_name='album',
            index=models.Index(fields=['album_title'], name='gallery_alb_album_t_c4357a_idx'),
        ),
    ]