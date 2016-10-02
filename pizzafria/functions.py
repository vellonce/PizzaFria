# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from blog.models import Post, Gallery
from podcast.models import EpisodePodcast


def make_posts_for_podcasts():
    episodes = EpisodePodcast.objects.all()
    user = User.objects.get(pk=1)
    for episode in episodes:
        picture = Gallery.objects.create(
            photo=episode.episode.original_image,
            title='',
            description=''
        )

        post = Post(
            entry_type=Post.PODCAST_EPISODE,
            title=episode.episode.title,
            subtitle=episode.episode.subtitle,
            published=episode.episode.published,
            intro=episode.episode.description[:256],
            content=episode.episode.description,
            main_image=picture,
            author=user,
        )
        post.save()
        episode.post = post
        episode.save()


def link_episodes_to_post():
    posts = Post.objects.all()
    for post in posts:
        episode = EpisodePodcast.objects.get(
            episode__title=post.title
        )
        episode.post = post
        episode.save()
