# -*- coding: utf-8 -*-
from podcast.models import EpisodePodcast, Tag


def generate_tags():
    episodes = EpisodePodcast.objects.exclude(
        episode__published__isnull=True)
    for episode in episodes:
        tags = episode.episode.keywords
        tags = tags.split(',')
        episode.tags.clear()
        for tag in tags:
            tag = tag.strip()
            tag, created = Tag.objects.get_or_create(tag=tag)
            episode.tags.add(tag)
        print episode.tags.all()
