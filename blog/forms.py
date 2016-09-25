# -*- coding: utf-8 -*-
from django import forms


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    # the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Tu nombre:"
        self.fields['contact_email'].label = "Tu correo:"
        self.fields['subject'].label = "Asunto:"
        self.fields['content'].label = "Qué nos quieres decir?"
