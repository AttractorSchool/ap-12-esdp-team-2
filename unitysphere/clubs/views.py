from django.views import generic
from . import models


class IndexView(generic.TemplateView):
    template_name = 'clubs/index.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_16_clubs'] = models.Club.objects.all().order_by('-members_count', '-likes_count')[:16]
        context['nearest_16_events'] = models.ClubEvent.objects.all().order_by('start_datetime')[:16]
        return context


class ClubDetailView(generic.DetailView):
    model = models.Club
    context_object_name = 'club'
    template_name = 'clubs/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link_1'] = 'СООБЩЕСТВА'
        context['link_1_url'] = '/#'
        context['link_2'] = self.get_object().name
        context['link_2_url'] = self.get_object().get_absolute_url()
        context['photos'] = models.ClubGalleryPhoto.objects.filter(club=self.get_object())
        context['services'] = models.ClubService.objects.filter(club=self.get_object())
        context['events'] = models.ClubEvent.objects.filter(club=self.get_object())
        return context
