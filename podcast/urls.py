# -*- coding: utf-8 -*-
__author__ = 'iwdev1'

from django.conf.urls import url, include

from .views import HomeEpisodeList, suscribe, EpisodeSingle

urlpatterns = [
    url(r'^$', HomeEpisodeList.as_view(),
        name='home'),
    url(r'^episode/(?P<slug>[-\w]+)$', EpisodeSingle.as_view(),
        name='episode_detail'),
    url(r"^feed/", include("podcasting.urls_feeds")),
    url(r'^suscribe$', suscribe,
        name='suscribe'),
]
