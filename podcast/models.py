# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Panelist(models.Model):
    name = models.CharField(max_length=128)
    alias = models.CharField(max_length=128)
    about = models.TextField()
    picture = models.ImageField(upload_to="panel")
    twitter = models.CharField(max_length=64)
    facebook = models.CharField(max_length=128)
    url = models.CharField(max_length=128)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=64)

    def __str__(self):
        return self.tag


@python_2_unicode_compatible
class Episode(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=140)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="episodes", null=True, blank=True)
    published = models.DateField()
    duration = models.CharField(max_length=64, null=True, blank=True)
    panel = models.ManyToManyField(Panelist)

    def __str__(self):
        return self.title
