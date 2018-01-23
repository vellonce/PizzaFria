from django.urls import re_path
from podcasting.views import ShowListView, ShowDetailView, EpisodeListView, EpisodeDetailView


urlpatterns = [
    re_path(r"^$", ShowListView.as_view(), name="podcasting_show_list"),
    re_path(
        r"^(?P<slug>[-\w]+)/$",
        ShowDetailView.as_view(),
        name="podcasting_show_detail"
    ),
    re_path(
        r"^(?P<show_slug>[-\w]+)/archive/$",
        EpisodeListView.as_view(),
        name="podcasting_episode_list"
    ),
    re_path(
        r"^(?P<show_slug>[-\w]+)/(?P<slug>[-\w]+)/$",
        EpisodeDetailView.as_view(),
        name="podcasting_episode_detail"
    ),
]
