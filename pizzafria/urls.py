# -*- coding: utf-8 -*-
import django.views.static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin


from podcast import urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(urls)),
    url(r"^podcasts/", include("podcasting.urls")),
    url(r"^feeds/podcasts/", include("podcasting.urls_feeds")),

    url(r'^static/(?P<path>.*)$', django.views.static.serve,
     {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
]
