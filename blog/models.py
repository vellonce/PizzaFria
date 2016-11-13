# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from PIL import Image
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.utils.six import python_2_unicode_compatible
from resizeimage import resizeimage
from tinymce.models import HTMLField

@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=64)

    def __str__(self):
        return self.tag


@python_2_unicode_compatible
class Gallery(models.Model):
    photo = models.ImageField(upload_to='images', verbose_name='Archivo')
    title = models.CharField(max_length=64, blank=True, verbose_name='Título')
    description = models.CharField(max_length=140, blank=True)

    def save(self, *args, **kwargs):
        if self.photo and not self.id:
            super(Gallery, self).save(*args, **kwargs)
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
                    with open(path, 'r+b') as f:
                        with Image.open(f) as image:
                            cover = resizeimage.resize_thumbnail(
                                image, size['size_arr'])
                            cover.save(new_path, image.format)
        else:
            super(Gallery, self).save(*args, **kwargs)

    def __str__(self):
        return 'image: ' + self.title


@python_2_unicode_compatible
class Post(models.Model):
    PODCAST_EPISODE = 'audio'
    VIDEO_CLIP = 'video'
    BLOG_POST = 'blog'
    POSTS_TYPES = (
        (VIDEO_CLIP, 'Video'),
        (PODCAST_EPISODE, 'Podcast'),
        (BLOG_POST, 'Post'),
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
    content = HTMLField(verbose_name='Contenido')
    main_image = models.ForeignKey(Gallery, related_name="main_images",
                                   verbose_name='Imagen principal (1400x1400)')
    images = models.ManyToManyField(Gallery)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, verbose_name='Autor')

    def __str__(self):
        return self.title + ' (' + self.entry_type + ')'


@python_2_unicode_compatible
class VideoPost(models.Model):
    post = models.ForeignKey(Post, verbose_name='Entrada')
    url = models.URLField(verbose_name='URL del video', blank=True, null=True)
    video_file = models.FileField(upload_to='videos', blank=True, null=True,
                                  verbose_name='Subir Video')

    def __str__(self):
        return "Video file: " + self.post.title
