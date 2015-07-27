from django.conf.urls import patterns, url

from podcasting.feeds import (
    RssShowFeed, AtomShowFeed, AtomRedirectView, RssRedirectView)
from podcasting.models import Enclosure


MIMES = "|".join([enclosure[0] for enclosure in Enclosure.MIME_CHOICES])


urlpatterns = patterns(
    "",

    # Episode list feed by show (RSS 2.0 and iTunes)
    url(r"^(?P<show_slug>[-\w]+)/(?P<mime_type>{mimes})/rss/$".format(mimes=MIMES),
        RssShowFeed(), name="podcasts_show_feed_rss"),

    # Episode list feed by show (Atom)
    url(r"^(?P<show_slug>[-\w]+)/(?P<mime_type>{mimes})/atom/$".format(mimes=MIMES),
        AtomShowFeed(), name="podcasts_show_feed_atom"),
)
