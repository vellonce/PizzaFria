# -*- coding: utf-8 -*-
from django.db.models import Model, CharField, SlugField, URLField,\
    TextField, ForeignKey, BooleanField, PROTECT
from django.utils.translation import ugettext_lazy as _


class Organization(Model):
    '''
        Organization/Authors of licenses.
    '''
    name = CharField(_('name'), max_length=100, unique=True,
        help_text=_('The complete name of a organization which is resposible for a license.'))
    slug = SlugField(_('slug'), unique=True)
    abbreviation = CharField(_('abbreviation'), max_length=50, blank=True,
        help_text=_('The short name of the organization.'))
    website = URLField(_('website'),
        help_text=_('The website of the organization.'))
    description = TextField(_('description'), blank=True,
        help_text=_('Additional information about the organization, that is not covered by the above fields.'))

    class Meta:
        db_table = 'licenses_organization'
        ordering = ('name', )
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    def __unicode__(self):
        return self.name

    def url(self):
        return self.website
    url = property(url)


class License(Model):
    '''
        A license.
    '''
    name = CharField(_('name'), max_length=200, unique=True,
        help_text=_('The full name of the license.'))
    slug = SlugField(_('slug'), unique=True)
    organization = ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='licenses',
        blank=True,
        null=True,
        on_delete=PROTECT
    )
    abbreviation = CharField(_('abbreviation'), max_length=50, blank=True,
        help_text=_('The short name of the license.'))
    url = URLField(_('url'),
        help_text=_('The URL to the legal text/online representation of the license.'))
    logo = URLField(_('logo'), blank=True,
        help_text=_('A logo/icon/badge that is clearly associated with the license.'))
    description = TextField(_('description'), blank=True)
    is_active = BooleanField(_('active'), default=True,
        help_text=_('Disable, if license shouldn\'t be available to users any more.'))

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'licenses_license'
        ordering = ('name', )
        verbose_name = _('license')
        verbose_name_plural = _('licenses')

    def shortest(self):
        return self.abbreviation or self.name
    shortest = property(shortest)
