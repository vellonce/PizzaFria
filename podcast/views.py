# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
from podcast.models import Episode


class EpisodeList(ListView):
    model = Episode
    paginate_by = 10
    template_name = "podcast/episodeguide.html"

    def get_queryset(self):
        return Episode.objects.all().order_by('-published')