# -*- coding: utf-8 -*-
__author__ = 'iwdev1'

from django.conf.urls import url, include

from blog.views import HomeEpisodeList, EpisodeSingle, get_posts, \
    PodcastList, VideoList, BlogList

urlpatterns = [
    url(r'^$', HomeEpisodeList.as_view(),
        name='home'),
    url(r'^slice/(?P<slug>[-\w]+)$', EpisodeSingle.as_view(),
        name='episode_detail'),
    url(r'^podcast/$', PodcastList.as_view(),
        name='podcast_list'),
    url(r'^video/$', VideoList.as_view(),
        name='video_list'),
    url(r'^blog/$', BlogList.as_view(),
        name='blog_list'),
    url(r"^feed/", include("podcasting.urls_feeds")),
    url(r'^get_posts/$', get_posts,
        name='get_posts'),
]
