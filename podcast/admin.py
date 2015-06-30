# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Panelist, Episode, Tag

admin.site.register(Panelist)
admin.site.register(Episode)
admin.site.register(Tag)
