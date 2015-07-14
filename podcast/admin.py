# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Panelist, EpisodePodcast, Tag, Suscriptor

admin.site.register(Panelist)
admin.site.register(EpisodePodcast)
admin.site.register(Tag)
admin.site.register(Suscriptor)