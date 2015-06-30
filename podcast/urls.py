# -*- coding: utf-8 -*-
__author__ = 'iwdev1'

from django.conf.urls import patterns, url

from .views import EpisodeList

urlpatterns = patterns(
    '',
    url(r'^$', EpisodeList.as_view(),
        name='create_payment_order'),
)
