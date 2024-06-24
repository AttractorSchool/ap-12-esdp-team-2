from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Case, When, Value, BooleanField
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from . import models
from calendar import HTMLCalendar


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
        context['events'] = models.ClubEvent.objects.annotate(
                                datetime_passed=Case(
                                    When(start_datetime__lt=timezone.now(), then=Value(True)),
                                    default=Value(False),
                                    output_field=BooleanField()
                                )
                            ).filter(club=self.get_object()).order_by('datetime_passed', 'start_datetime')
        return context


class ClubListView(generic.ListView):
    model = models.Club
    context_object_name = 'clubs'
    template_name = 'clubs/clubs.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link_1'] = 'СООБЩЕСТВА'
        context['link_1_url'] = reverse('clubs')
        context['search'] = self.request.GET.get('search')
        context['categories'] = models.ClubCategory.objects.all()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            return qs.filter(name__icontains=search_query)
        return qs


class CategoryClubsView(generic.DetailView):
    model = models.ClubCategory
    context_object_name = 'category'
    template_name = 'clubs/clubs.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clubs_list = models.Club.objects.filter(category=self.get_object())
        search_query = self.request.GET.get('search')
        context['search'] = search_query
        if search_query:
            clubs_list = clubs_list.filter(name__icontains=search_query)
        page_obj = self.get_paginator(clubs_list)
        context['link_1'] = self.object.name
        context['link_1_url'] = reverse('clubs')
        context['categories'] = models.ClubCategory.objects.all()
        context['is_paginated'] = page_obj.has_other_pages()
        context['page_obj'] = context['clubs'] = page_obj
        return context

    def get_paginator(self, clubs_list):
        paginator = Paginator(clubs_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return page_obj


class EventCalendarView(generic.ListView):
    model = models.ClubEvent
    context_object_name = 'events'
    template_name = 'clubs/event_calendar.html'
