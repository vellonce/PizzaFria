from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from django.contrib.sites.models import Site


class EpisodeManagerQuerySet(QuerySet):
    """Returns public episodes that are currently activated."""

    def itunespublished(self):
        return self.exclude(Q(published=None) | Q(block=True))

    def published(self):
        return self.exclude(published=None)

    def onsite(self):
        return self.filter(shows__sites=Site.objects.get_current())

    def current(self):
        try:
            return self.published().order_by("-published")[0]
        except IndexError:
            return None


class EpisodeManager(models.Manager):
    def get_queryset(self):
        return EpisodeManagerQuerySet(self.model, using=self._db)

    def itunespublished(self):
        return self.get_queryset().itunespublished()

    def published(self):
        return self.get_queryset().published()

    def onsite(self):
        return self.get_queryset().onsite()

    def current(self):
        return self.get_queryset().current()


class ShowManagerQuerySet(models.query.QuerySet):
    """Returns shows that are on the current site."""
    def published(self):
        return self.exclude(published=None)

    def onsite(self):
        return self.filter(sites=Site.objects.get_current())


class ShowManager(models.Manager):
    def get_queryset(self):
        return ShowManagerQuerySet(self.model, using=self._db)

    def onsite(self):
        return self.get_queryset().onsite()
