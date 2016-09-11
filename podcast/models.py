# -*- coding: utf-8 -*-
import os

import audiotools
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from pymediainfo import MediaInfo
from slugify import slugify
from podcasting.models import Episode as EpisodePodcasting, EmbedMedia, \
    Enclosure


@python_2_unicode_compatible
class MediaAccount(models.Model):
    SOCIAL_MEDIA = (
        ('fa-facebook', 'Facebook'),
        ('fa-twitter', 'Twitter'),
        ('fa-snapchat-ghost', 'Snapchat'),
        ('fa-instagram', 'Instagram'),
        ('fa-link', 'Otro'),
    )
    social_network = models.CharField(max_length=64, choices=SOCIAL_MEDIA)
    user_url = models.URLField()

    def __str__(self):
        return self.user_url


@python_2_unicode_compatible
class Panelist(models.Model):
    name = models.CharField(max_length=128)
    alias = models.CharField(max_length=128, blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    short_bio = models.TextField(null=True, blank=True)
    role = models.CharField(null=True, blank=True, max_length=64)
    picture = models.ImageField(upload_to="panel", null=True, blank=True)
    social_media = models.ManyToManyField(MediaAccount)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=64)

    def __str__(self):
        return self.tag


@python_2_unicode_compatible
class EpisodePodcast(models.Model):
    episode = models.ForeignKey(EpisodePodcasting)
    number_of_episode = models.CharField(max_length=10, default='00')
    file = models.FileField(upload_to="episodes", null=True, blank=True)
    panel = models.ManyToManyField(Panelist)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.episode.title

    def save(self, *args, **kwargs):
        super(EpisodePodcast, self).save(*args, **kwargs)
        tags = self.episode.keywords
        tags = tags.split(',')
        self.tags.clear()
        for tag in tags:
            tag = tag.strip()
            tag, created = Tag.objects.get_or_create(tag=tag)
            self.tags.add(tag)

        if self.file:
            url = 'http://{0}{1}'.format(settings.SITE_URL, self.file.url)
            em = EmbedMedia.objects.filter(episode=self.episode)
            if not em:
                em = EmbedMedia(
                    episode=self.episode,
                    url=url
                )
            else:
                em = em[0]
                if em.url != url:
                    em.url = url
            em.save()

            size = os.path.getsize(self.file.path)
            file_ext = self.file.name.split('.')[-1].lower().strip()
            if file_ext in Enclosure.ALLOWEWD_MIMES:
                audiofile = audiotools.open(self.file.path)
                info = MediaInfo.parse(self.file.path)
                # Just guessing here, usig this as default if cannot get
                # the bitrate
                bitrate = 192
                for track in info.tracks:
                    if track.track_type == 'General':
                        pass
                    if track.track_type == 'Audio':
                        bitrate = track.bit_rate / 1000
                enclosure = Enclosure(
                    url=url,
                    size=size,
                    mime=file_ext,
                    bitrate=bitrate,
                    sample=audiofile.sample_rate(),
                    channel=audiofile.channels(),
                    duration=int(audiofile.seconds_length()),
                )
                enclosure.save()
                enclosure.episodes.add(self.episode)
            else:
                raise TypeError("File not supported for podcasting")

    class Meta:
        ordering = ["-episode__published"]


@python_2_unicode_compatible
class Suscriptor(models.Model):
    email = models.EmailField(max_length=128)

    def __str__(self):
        return self.email