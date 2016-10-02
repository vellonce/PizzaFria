# -*- coding: utf-8 -*-
from podcast.models import EpisodePodcast
from .models import Post


def latest_entries(request):
    last = Post.objects.filter(
        entry_type=Post.PODCAST_EPISODE,
        published__isnull=False
    ).order_by('-published').first()
    if last:
        last = EpisodePodcast.objects.get(post=last)

    latest = Post.objects.filter(
        published__isnull=False
    ).order_by('-published')
    number_of_entries = 2
    return {
        'latest_entries': latest[:number_of_entries],
        'latest': last
    }
