# -*- coding: utf-8 -*-
from podcast.models import Suscriptor

__author__ = 'iwdev1'

from django.forms import ModelForm, EmailInput


class SuscriptionForm(ModelForm):
    class Meta:
        model = Suscriptor
        fields = ['email']
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Email',
                                       'class': 'form-control'}),
        }
