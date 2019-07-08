from podcast.models import EpisodePodcast
from blog.models import Post


def home_elements():
    last = EpisodePodcast.objects.exclude(
        episode__published__isnull=True).first()
    return Post.objects.exclude(
        published=None
    ).exclude(
        pk=last.post.pk
    ).order_by('-published')
