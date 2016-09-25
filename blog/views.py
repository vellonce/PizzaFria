# Create your views here.
from django.core.mail import send_mail
from django.views.generic import TemplateView, FormView

from blog.forms import ContactForm
from podcast.models import Panelist


class AboutView(TemplateView):
    template_name = 'podcast/about_us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['panelists'] = Panelist.objects.filter(status=True)
        return context


class ThanksView(TemplateView):
    template_name = 'podcast/thanks.html'


class ContactView(FormView):
    template_name = 'podcast/contact_us.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        contact_name = form.cleaned_data.get(
            'contact_name', '')
        contact_email = form.cleaned_data.get(
            'contact_email', '')
        subject = form.cleaned_data.get(
            'subject', '')
        form_content = form.cleaned_data.get('content', '')
        form_content = contact_name + ' dice: ' + form_content
        send_mail(
            subject,
            form_content,
            contact_email,
            ['hellocutiepie@pizzafria.com'],
            fail_silently=False,
        )
        return super(ContactView, self).form_valid(form)
