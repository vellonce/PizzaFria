# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from slugify import slugify
from podcasting.models import Episode as EpisodePodcasting


@python_2_unicode_compatible
class Panelist(models.Model):
    name = models.CharField(max_length=128)
    alias = models.CharField(max_length=128, blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="panel", null=True, blank=True)
    twitter = models.CharField(max_length=64, null=True, blank=True)
    facebook = models.CharField(max_length=128, null=True, blank=True)
    url = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=64)

    def __str__(self):
        return self.tag


@python_2_unicode_compatible
class Episode(models.Model):
    episode = models.ForeignKey(EpisodePodcasting)
    number_of_episode = models.CharField(max_length=10, default='00')
    panel = models.ManyToManyField(Panelist)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Episode, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/%i/" % self.slug


@python_2_unicode_compatible
class Suscriptor(models.Model):
    email = models.EmailField(max_length=128)

    def __str__(self):
        return self.email