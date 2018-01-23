# -*- coding: utf-8 -*-
from django.db.models import ForeignKey
from django.utils.translation import ugettext_lazy as _


class LicenseField(ForeignKey):
    """
    A ForeignKey field with default value for verbose_name
    and a shortcut for switching blank/null to True.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', _('license'))
        if kwargs.pop('required', None) == False:
            kwargs['blank'] = True
            kwargs['null'] = True
        super(LicenseField, self).__init__('licenses.License', *args, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^licenses\.fields\.LicenseField'])
except ImportError:
    pass
