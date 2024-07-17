from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Case, When, Value, BooleanField
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from . import models, forms
from calendar import HTMLCalendar

from .api.serializers import club
from .mixins import ClubRelatedObjectCreateMixin


class IndexView(generic.TemplateView):
    template_name = 'clubs/index.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_16_clubs'] = models.Club.objects.all().order_by('-members_count', '-likes_count')[:16]
        context['nearest_16_events'] = models.ClubEvent.objects.all().order_by('start_datetime')[:16]
        return context
    
def join_club(request, club_id):
    club = get_object_or_404(models.Club, id=club_id)
    user = request.user
    
    club.members.add(user)
    club.members_count += 1
    club.save()
    
    if club.whatsapp_link:
        return redirect(club.get_whatsapp_link())
    
    return redirect('club_detail', pk=club.id)

class ClubDetailView(generic.DetailView):
    model = models.Club
    context_object_name = 'club'
    template_name = 'clubs/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.get_object().name}'
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
    paginate_by = 40

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ВСЕ СООБЩЕСТВА'
        context['search'] = self.request.GET.get('search')
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            return qs.filter(name__icontains=search_query)
        return qs


class ClubCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Club
    template_name = 'clubs/create_club.html'
    form_class = forms.ClubForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Создать сообщество'
        return ctx

    def form_valid(self, form):
        if form.is_valid():
            club = form.save(commit=False)
            club.creater = self.request.user
            club.members_count += 1
            club.save()
            club.managers.add(self.request.user)
            club.members.add(self.request.user)
            return redirect(club.get_absolute_url())
        else:
            return super().form_invalid(form)


class ClubEditView(PermissionRequiredMixin, generic.UpdateView):
    model = models.Club
    template_name = 'clubs/create_club.html'
    form_class = forms.ClubUpdateForm

    def has_permission(self):
        return self.request.user in self.get_object().managers.all()


class ChooseClubManagersView(PermissionRequiredMixin, generic.UpdateView):
    model = models.Club
    template_name = 'clubs/choose_club_managers.html'
    form_class = forms.SelectClubManagersForm

    def has_permission(self):
        return self.request.user in self.get_object().managers.all()

    def form_valid(self, form):
        users_after = form.data.getlist('managers')
        check = self.form_class.required_at_least_one_manager
        if form.is_valid() and check(users_after, form):
            self.get_object().managers.set(form.cleaned_data.get('managers'))
            return redirect(self.get_object().get_absolute_url())
        else:
            return render(self.request, self.template_name, context={'form': form})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['page_title'] = 'Добавление/удаление руководителей'
        return ctx

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'managers': self.get_object().managers.all()})
        form.fields['managers'].queryset = self.get_object().members.all().union(self.get_object().managers.all())
        return self.render_to_response({'form': form})


class CategoryClubsView(generic.DetailView):
    model = models.ClubCategory
    context_object_name = 'category'
    template_name = 'clubs/clubs.html'
    paginate_by = 40

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clubs_list = models.Club.objects.filter(category=self.get_object())
        search_query = self.request.GET.get('search')
        context['search'] = search_query
        if search_query:
            clubs_list = clubs_list.filter(name__icontains=search_query)
        page_obj = self.get_paginator(clubs_list)
        context['page_title'] = self.object.name
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


class ClubEventListView(generic.ListView):
    model = models.ClubEvent
    context_object_name = 'events'
    template_name = 'clubs/club_events.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'События клубов'
        return ctx

    def get_queryset(self):
        qs = models.ClubEvent.objects.annotate(
            datetime_passed=Case(
                When(start_datetime__lt=timezone.now(), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('datetime_passed', 'start_datetime')
        return qs


class EventDetailView(generic.DetailView):
    model = models.ClubEvent
    context_object_name = 'event'
    template_name = 'clubs/event_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = self.get_object().title
        return ctx


class CreateClubEventView(ClubRelatedObjectCreateMixin, PermissionRequiredMixin, generic.CreateView):
    model = models.ClubEvent
    form_class = forms.CreateClubEventForm
    template_name = 'clubs/create_event.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'Организация события от клуба - {self.get_club()}'
        return ctx


class ClubServiceListView(generic.ListView):
    model = models.ClubService
    context_object_name = 'services'
    template_name = 'clubs/club_services.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Услуги клубов'
        return ctx
    

class CreateServiceView(generic.CreateView):
    model = models.ClubService
    form_class = forms.ClubServiceCreateForm
    template_name = 'clubs/create_service.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Создать услугу'
        return ctx
    
    def form_valid(self, form):
        if form.is_valid():
            service = form.save(commit=False)
            club_id = self.kwargs.get('pk')
            club = models.Club.objects.get(id=club_id)
            service.club = club
            service.save()
            photo = form.cleaned_data.get('photo')
            photo_obj = models.ClubServiceImage.objects.create(
                service=service,
                image=photo
            )
            return redirect('index')
        else:
            return super().form_invalid(form)
        


class UpdateServiceView(generic.UpdateView):
    model = models.ClubService
    form_class = forms.ClubServiceCreateForm
    template_name = 'clubs/update_service.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Редактировать услугу'
        ctx['service'] = self.object
        return ctx
    
    def form_valid(self, form):
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            photo = form.cleaned_data.get('photo')
            if photo:
                photo_obj, created = models.ClubServiceImage.objects.get_or_create(
                    service=service
                )
                photo_obj.image = photo
                photo_obj.save()
            return redirect('index')
        else:
            return super().form_invalid(form)
        

class ClubServiceDetailView(generic.DetailView):
    model = models.ClubService
    template_name = 'clubs/detail_service.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.name
        return context


class EventCalendarView(generic.ListView):
    model = models.ClubEvent
    context_object_name = 'events'
    template_name = 'clubs/event_calendar.html'


class AboutView(generic.TemplateView):
    template_name = 'clubs/about.html'


class ClubPhotoGalleryView(generic.ListView):
    model = models.ClubGalleryPhoto
    context_object_name = 'photos'
    template_name = 'clubs/club_photogallery.html'
    paginate_by = 40

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        club = models.Club.objects.get(id=self.kwargs.get('pk'))
        ctx['page_title'] = f'{club} - Фотогалерея'
        ctx['club'] = club
        return ctx

    def get_queryset(self):
        club = models.Club.objects.get(id=self.kwargs.get('pk'))
        return self.model.objects.filter(club=club)


class ClubAddPhotoView(ClubRelatedObjectCreateMixin, PermissionRequiredMixin, generic.CreateView):
    model = models.ClubGalleryPhoto
    form_class = forms.AddGalleryPhotoForm
    template_name = 'clubs/club_add_photo.html'

    def get_success_url(self):
        return self.get_club().get_gallery_url()
