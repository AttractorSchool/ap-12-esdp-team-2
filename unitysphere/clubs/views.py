from django.views import generic
from . import models


class IndexView(generic.TemplateView):
    template_name = 'clubs/index.html'
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['top_16_clubs'] = models.Club.objects.all().order_by('-members_count', '-likes_count')[:16]
        context['nearest_16_events'] = models.ClubEvent.objects.all().order_by('start_datetime')[:16]
        return context


class ClubDetailView(generic.DetailView):
    model = models.Club
    context_object_name = 'club'
    template_name = 'clubs/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClubDetailView, self).get_context_data(**kwargs)
        cont