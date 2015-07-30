# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

# Create your views here.
from podcast.forms import SuscriptionForm
from podcast.models import EpisodePodcast, Suscriptor


class EpisodeList(ListView):
    model = EpisodePodcast
    paginate_by = 10
    template_name = "podcast/episodeguide.html"

    def get_context_data(self, **kwargs):
        context = super(EpisodeList, self).get_context_data(**kwargs)
        context['suscribe'] = SuscriptionForm(None)
        context['message'] = self.request.GET.get('message', None)

        return context


def suscribe(request):
    if request.method != 'POST':
        return render(request, "nothinghere.html")
    suscriber = SuscriptionForm(request.POST)
    if suscriber.is_valid():
        email = suscriber.cleaned_data['email']
        Suscriptor.objects.get_or_create(email=email)
        message = "Tu registro ha sido exitoso, " \
                  "te enviaremos un correo cuando el próximo episodio " \
                  "esté en línea"
    else:
        message = "Tu correo es incorrecto, por favor verificalo"
    return custom_redirect('episode_list', message=message)


def custom_redirect(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse
    import urllib
    url = reverse(url_name, args = args)
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


class EpisodeSingle(DetailView):
    template_name = "podcast/episodesingle.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_field, None)
        if slug:
            EpisodePodcast.objects.get(episode__slug=slug)

    def get_context_data(self, **kwargs):
        context = super(EpisodeSingle, self).get_context_data(**kwargs)
        context['suscribe'] = SuscriptionForm(None)
        context['message'] = self.request.GET.get('message', None)

        return context
