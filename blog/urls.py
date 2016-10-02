# -*- coding: utf-8 -*-
__author__ = 'iwdev1'

from django.conf.urls import url, include

from blog.views import HomeEpisodeList, EpisodeSingle, get_posts

urlpatterns = [
    url(r'^$', HomeEpisodeList.as_view(),
        name='home'),
    url(r'^episode/(?P<slug>[-\w]+)$', EpisodeSingle.as_view(),
        name='episode_detail'),
    url(r"^feed/", include("podcasting.urls_feeds")),
    url(r'^get_posts/$', get_posts,
        name='get_posts'),

]
