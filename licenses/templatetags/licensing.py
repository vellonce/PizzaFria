# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from licenses.models import License

register = template.Library()


class GetLicenseNode(template.Node):
    '''
        Generic node to get one license, the tag defines the search paramter.
    '''

    def handle_token(cls, parser, token, field):
        tokens = token.split_contents()
        if len(tokens) == 4:
            if tokens[2] != 'as':
                raise template.TemplateSyntaxError("Second argument in %s must be 'as'" % tokens[0])
            lookup = tokens[1]
            # trim quotation marks
            if (lookup[0] == '"' and lookup[-1] == '"') or (lookup[0] == "'" and lookup[-1] == "'"):
                lookup = lookup[1:-1]
            return cls(lookup=lookup, varname=tokens[3], field=field)
        else:
            raise template.TemplateSyntaxError("%r tag requires 3 arguments" % tokens[0])
    handle_token = classmethod(handle_token)

    def __init__(self, lookup=None, varname=None, field=None):
        self.varname = varname
        self.lookup = lookup
        self.field = field

    def render(self, context):
        try:
            lookup_dict = {self.field: self.lookup}
            license = License.objects.filter(**lookup_dict)[0]
        except IndexError:
            license = None
        context[self.varname] = license
        return ''


def get_license_by_abbr(parser, token):
    '''
        Get a license via it's abbreviation and save it to ´varname´.

        Usage: {% get_license_by_abbr "short_name" as varname %}
        Quotation marks are optional.
    '''
    return GetLicenseNode.handle_token(parser, token, field='abbreviation')
register.tag('get_license_by_abbr', get_license_by_abbr)
register.tag('get_license_by_abbreviation', get_license_by_abbr)


def get_license_by_slug(parser, token):
    '''
        Get a license via it's slug and save it to ´varname´.

        Usage: {% get_license_by_slug "slug" as varname %}
        Quotation marks are optional.
    '''
    return GetLicenseNode.handle_token(parser, token, field='slug')
register.tag('get_license_by_slug', get_license_by_slug)


def license_link(license):
    '''
        Displays the license as a hyperlink.

        Usage {{ license|license_link }}
    '''
    return render_to_string('licenses/link.html', {
        'name': conditional_escape(license.name),
        'url': conditional_escape(license.url),
    })
register.filter('license_link', license_link)


def license_short_link(license):
    '''
        Displays the license as a hyperlink and uses the abbreviation as
        innerHtml if available.

        Usage {{ license|license_short_link }}
    '''
    return render_to_string('licenses/short_link.html', {
        'abbr': conditional_escape(license.shortest),
        'url': conditional_escape(license.url),
    })
register.filter('license_short_link', license_short_link)
register.filter('license_abbr_link', license_short_link)


def license_logo(license):
    '''
        Displays the license as a hyperlink with an images as innerHtml.

        Usage {{ license|license_logo }}
    '''
    return render_to_string('licenses/logo.html', {
        'name': conditional_escape(license.name),
        'url': conditional_escape(license.url),
        'abbr': conditional_escape(license.shortest),
        'img': conditional_escape(license.logo),
    })
register.filter('license_logo', license_logo)
