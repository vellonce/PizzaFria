# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from PIL import Image
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from resizeimage import resizeimage


class Tag(models.Model):
    tag = models.CharField(max_length=64)

    def __str__(self):
        return self.tag


class Gallery(models.Model):
    photo = models.ImageField(upload_to='images', verbose_name='Archivo')
    title = models.CharField(max_length=64, blank=True, verbose_name='Título')
    description = models.CharField(max_length=140)

    def save(self, *args, **kwargs):
        if self.photo and not self.id:
            path = self.photo.path
            print path
            image_name = path.split('/')
            image_name = image_name[-1]
            base_path = path[:-len(image_name)]
            if path.endswith('.jpg') or path.endswith('.jpeg') or \
                    path.endswith('.png'):
                sizes = [
                    dict(size='small', size_arr=[285, 202]),
                    dict(size='medium', size_arr=[555, 416]),
                    dict(size='full', size_arr=[1400, 1400])
                ]
                for size in sizes:
                    new_path = base_path + size['size'] + image_name
                    with open(new_path, 'r+b') as f:
                        with Image.open(f) as image:
                            cover = resizeimage.resize_thumbnail(
                                image, size['size_arr'])
                            cover.save(new_path, image.format)
        super(Gallery, self).save(*args, **kwargs)


class Post(models.Model):
    POSTS_TYPES = (
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('blog', 'Entrada de Blog'),
    )
    entry_type = models.CharField(max_length=64, choices=POSTS_TYPES)
    title = models.CharField(max_length=128, verbose_name='Título')
    subtitle = models.CharField(max_length=128, verbose_name='Sub Título',
                                blank=True)
    slug = AutoSlugField("slug", populate_from="title", unique="True")
    published = models.DateTimeField(verbose_name='Publicado el', null=True)
    intro = models.TextField(
        max_length=256,
        verbose_name='Texto introductorio',
        help_text='preferentemente corto. Texto para mostrar en página '
                  'como previo')
    content = models.TextField(verbose_name='Contenido')
    images = models.ManyToManyField(Gallery)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, verbose_name='Autor')

    def __str__(self):
        return self.title + ' (' + self.entry_type + ')'
