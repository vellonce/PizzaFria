# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, site, HORIZONTAL
from django.utils.translation import ugettext_lazy as _
from licenses.models import Organization, License


class OrganizationAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'abbreviation', 'website')
    search_fields = ('name', 'slug', 'abbreviation', 'website', 'description')
site.register(Organization, OrganizationAdmin)


class LicenseAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'abbreviation', 'organization', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('name', 'slug', 'abbreviation', 'url', 'description')
    radio_fields = {'organization': HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'url', 'abbreviation', 'organization'),
        }),
        (_('Advanced options'), {
            'classes': ('collapse', ),
            'fields': ('logo', 'description', 'is_active'),
        }),
    )
site.register(License, LicenseAdmin)
