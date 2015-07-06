# -*- coding: utf-8 -*-
__author__ = 'iwdev1'

from django.conf.urls import patterns, url

from .views import EpisodeList, EpisodeSingle, suscribe

urlpatterns = patterns(
    '',
    url(r'^$', EpisodeList.as_view(),
        name='episode_list'),
    url(r'^(?P<slug>[-\w]+)$', EpisodeSingle.as_view(),
        name='episode_detail'),
    url(r'^suscribe$', suscribe,
        name='suscribe'),
)
