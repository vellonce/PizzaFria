# -*- coding: utf-8 -*-

from django.urls import path, include, re_path
from rest_framework import routers
from blog.api import


urlpatterns = [
    re_path(r'^episodes/$', HomeEpisodeList.as_view(), name='home'),
    re_path(
        r'^slice/(?P<slug>[-\w]+)$',
        EpisodeSingle.as_view(),
        name='episode_detail'
    ),
    re_path(r'^podcast/$', PodcastList.as_view(), name='podcast_list'),
    re_path(r'^video/$', VideoList.as_view(), name='video_list'),
    re_path(r'^blog/$', BlogList.as_view(), name='blog_list'),
    re_path(r'^search/$', SearchList.as_view(), name='search_list'),
    path("feed/", include("podcasting.urls_feeds")),
    re_path(r'^get_posts/$', get_posts, name='get_posts'),
]
