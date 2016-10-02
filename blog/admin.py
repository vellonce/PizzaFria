# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Post, Gallery

admin.site.register(Post)
admin.site.register(Gallery)
