# -*- coding: utf-8 -*-
import django.views.static
from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin

from blog import urls, api_urls
from blog.views import AboutView, ContactView, ThanksView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('', include(urls)),
    re_path(r'^about/$', AboutView.as_view(), name='about'),
    re_path(r'^contact_us/$', ContactView.as_view(), name='contact_us'),
    re_path(r'^thanks/$', ThanksView.as_view()),
    path('podcasts/', include("podcasting.urls")),
    path('feeds/podcasts/', include("podcasting.urls_feeds")),

    path('tinymce/', include('tinymce.urls')),

    re_path(r'^static/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
]
