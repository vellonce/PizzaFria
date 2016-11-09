# Create your views here.
import json
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.datetime_safe import strftime
from django.views.generic import TemplateView, FormView, ListView, DetailView

from blog.forms import ContactForm
from oembed_consumer import Consumer
from podcast.models import EpisodePodcast, Panelist
from podcasting.models import Show
from .models import Post, VideoPost


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


class HomeEpisodeList(ListView):
    model = Post
    paginate_by = 7
    template_name = "podcast/home.html"

    def get_queryset(self):
        last = EpisodePodcast.objects.exclude(
            episode__published__isnull=True).first()
        episodes = Post.objects.exclude(
            published=None
        ).exclude(
            pk=last.post.pk
        ).order_by('-published')

        return episodes

    def get_context_data(self, **kwargs):
        context = super(HomeEpisodeList, self).get_context_data(**kwargs)
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


class PodcastList(ListView):
    template_name = 'podcast/podcast_list.html'
    paginate_by = 10

    def get_queryset(self):
        episodes = Post.objects.exclude(
            published=None
        ).filter(
            entry_type=Post.PODCAST_EPISODE
        ).order_by('-published')
        return episodes

    def get_context_data(self, **kwargs):
        context = super(PodcastList, self).get_context_data(**kwargs)
        context['type'] = 'audio'
        return context


class VideoList(ListView):
    template_name = 'podcast/podcast_list.html'

    def get_queryset(self):
        episodes = Post.objects.exclude(
            published=None
        ).filter(
            entry_type=Post.VIDEO_CLIP
        ).order_by('-published')
        return episodes

    def get_context_data(self, **kwargs):
        context = super(VideoList, self).get_context_data(**kwargs)
        context['type'] = 'video'
        return context


class BlogList(ListView):
    template_name = 'podcast/podcast_list.html'

    def get_queryset(self):
        episodes = Post.objects.exclude(
            published=None
        ).filter(
            entry_type=Post.BLOG_POST
        ).order_by('-published')
        return episodes

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['type'] = 'blog'
        return context



class DateTimeEncoder(json.JSONEncoder):
    # default JSONEncoder cannot serialize datetime.datetime objects
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = obj.strftime('%Y-%m-%d')
        else:
            encoded_object = super(self, obj)
        return encoded_object


def get_posts(request):
    # start
    offset = request.GET.get('offset', 8)
    # take the next x elements following start
    take = request.GET.get('take', 6)
    final_offset = int(offset) + int(take)
    last = EpisodePodcast.objects.exclude(
        episode__published__isnull=True).first()
    posts = Post.objects.exclude(
        published=None,
        pk=last.post.pk
    ).order_by('-published')
    posts = posts[offset:final_offset]
    post_list = []
    for post in posts:
        published = strftime(post.published, '%Y-%m-%d')
        tags = post.tags.all()
        post_dict = dict(
            title=post.title,
            subtitle=post.subtitle,
            slug=post.subtitle,
            published=published,
            intro=post.intro,
            main_image__photo=post.main_image.photo.url,
            entry_type=post.entry_type,
            tags=[tag.tag for tag in tags]
        )
        post_list.append(post_dict)
    response = dict(
        offset=final_offset,
        posts=list(post_list)
    )
    return JsonResponse(response, safe=False)



class EpisodeSingle(DetailView):
    template_name = "podcast/episode_single.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_field, None)
        if slug:
            return Post.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        context = super(EpisodeSingle, self).get_context_data(**kwargs)
        context['show'] = Show.objects.first().slug
        context['feed_type'] = 'mp3'
        context['itunes_url'] = settings.ITUNES_URL
        context['domain'] = settings.PODCAST_DOMAIN
        next_episode = Post.objects.filter(
            pk__gt=self.object.pk
        ).exclude(
            published__isnull=True
        ).order_by('pk')

        next_episode = next_episode.first()

        prev_episode = Post.objects.filter(
            pk__lt=self.object.pk
        ).exclude(
            published__isnull=True
        ).order_by('-pk')
        prev_episode = prev_episode.first()

        context['next'] = next_episode
        context['prev'] = prev_episode

        # Time marks
        time_marks = []
        if self.object.entry_type == Post.PODCAST_EPISODE:
            episode = self.object.episodepodcast_set.first()
            context['episode'] = episode
            context['minutes'] = episode.episode.hours * 60 + \
                                 episode.episode.minutes
            episode = episode.episode

            timemarks = episode.tracklist
            if timemarks:
                timemarks = timemarks.splitlines()
                for timemark in timemarks:
                    timemark = timemark.split('-')
                    try:
                        seconds = timemark[0]
                        mark = timemark[1]
                    except ValueError:
                        print 'malformed timemark', timemark
                        continue
                    m, s = divmod(int(seconds), 60)
                    h, m = divmod(m, 60)
                    if h:
                        human_time = "%d:%02d:%02d" % (h, m, s)
                    else:
                        human_time = "%02d:%02d" % (m, s)
                    time_marks.append(dict(human_time=human_time,
                                           seconds=seconds, mark=mark))
        elif self.object.entry_type == Post.VIDEO_CLIP:
            video = VideoPost.objects.get(post=self.object)
            context['episode'] = video
            if video.video_file:
                context['type'] = 'player'
            else:
                context['type'] = 'embed'
                consumer = Consumer()
                # This returns a dict with the oembed data
                embed = consumer.get_oembed(video.url)
                print embed
                context['embed'] = embed[0].get('html', None)
                context['embed'].replace()

        context['time_marks'] = time_marks
        return context
