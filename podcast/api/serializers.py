from rest_framework import serializers
from podcast.models import EpisodePodcast


class EpisodePodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodePodcast
