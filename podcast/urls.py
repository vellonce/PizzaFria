# -*- coding: utf-8 -*-
__author__ = 'iwdev1'

from django.conf.urls import patterns, url, include

from .views import EpisodeList, suscribe, EpisodeSingle

urlpatterns = patterns(
    '',
    url(r'^$', EpisodeList.as_view(),
        name='episode_list'),
    url(r'^(?P<slug>[-\w]+)$', EpisodeSingle.as_view(),
        name='episode_detail'),

    url(r"^podcasts/", include("podcasting.urls")),
    url(r"^feeds/podcasts/", include("podcasting.urls_feeds")),
    url(r'^suscribe$', suscribe,
        name='suscribe'),
)
