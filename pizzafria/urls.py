# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin

from podcast import urls
from feed import urls as feed_urls

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(urls)),
    #url(r'^feed/', include(feed_urls)),
    url(r"^podcasts/", include("podcasting.urls")),
    url(r"^feeds/podcasts/", include("podcasting.urls_feeds")),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
