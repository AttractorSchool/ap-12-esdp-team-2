from django.shortcuts import redirect
from django.views import generic

from clubs import forms, models


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
            models.ClubServiceImage.objects.create(
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
