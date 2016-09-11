# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

# Create your views here.
from podcasting.models import Show
from podcast.forms import SuscriptionForm
from podcast.models import EpisodePodcast, Suscriptor, Panelist, Tag


class HomeEpisodeList(ListView):
    model = EpisodePodcast
    paginate_by = 10
    template_name = "podcast/home.html"

    def get_queryset(self):
        last = EpisodePodcast.objects.exclude(
            episode__published__isnull=True).first()
        episodes = EpisodePodcast.objects.exclude(
            pk=last.pk).exclude(episode__published=None)[:7]
        return episodes

    def get_context_data(self, **kwargs):
        context = super(HomeEpisodeList, self).get_context_data(**kwargs)
        context['suscribe'] = SuscriptionForm(None)
        context['message'] = self.request.GET.get('message', None)
        context['show'] = Show.objects.first().slug
        context['feed_type'] = 'mp3'
        context['itunes_url'] = settings.ITUNES_URL
        context['domain'] = settings.PODCAST_DOMAIN
        context['latest'] = EpisodePodcast.objects.exclude(
            episode__published__isnull=True).first()
        context['main_tags'] = context['latest'].episode.keywords.split(',')
        context['panelists'] = Panelist.objects.filter(status=True)


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
    template_name = "podcast/episode_single.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_field, None)
        if slug:
            return EpisodePodcast.objects.get(episode__slug=slug)

    def get_queryset(self):
        last = EpisodePodcast.objects.exclude(
            episode__published__isnull=True).first()
        episodes = EpisodePodcast.objects.exclude(
            pk=last.pk).exclude(episode__published=None)[:7]
        return episodes

    def get_context_data(self, **kwargs):
        context = super(EpisodeSingle, self).get_context_data(**kwargs)
        context['suscribe'] = SuscriptionForm(None)
        context['message'] = self.request.GET.get('message', None)
        context['show'] = Show.objects.first().slug
        context['feed_type'] = 'mp3'
        context['itunes_url'] = settings.ITUNES_URL
        context['domain'] = settings.PODCAST_DOMAIN
        context['latest'] = EpisodePodcast.objects.exclude(
            episode__published__isnull=True).first()
        context['second'] = EpisodePodcast.objects.exclude(
            episode__published__isnull=True
        ).exclude(
            pk=context['latest'].pk).first()
        return context


def generate_tags():
    episodes = EpisodePodcast.objects.exclude(
        episode__published__isnull=True)
    for episode in episodes:
        tags = episode.episode.keywords
        tags = tags.split(',')
        episode.tags.clear()
        for tag in tags:
            tag = tag.strip()
            tag, created = Tag.objects.get_or_create(tag=tag)
            episode.tags.add(tag)
        print episode.tags.all()
