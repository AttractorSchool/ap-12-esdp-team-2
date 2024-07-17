from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from .forms import RegisterUserForm, UserLoginForm, UserUpdateForm
from .models import User
from clubs.models import ClubCategory


class RegisterUserView(generic.FormView):
    form_class = RegisterUserForm
    template_name = 'accounts/register_user.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Центр сообществ - Регистрация'
        return ctx

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        else:
            return super().form_invalid(form)


class LoginUserView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login_user.html'


class UserDetailView(generic.DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = self.get_object()
        ctx['categories'] = ClubCategory.objects.all()
        return ctx


class UserListView(generic.ListView):
    model = User
    context_object_name = 'users'
    template_name = 'accounts/user_list.hmtl'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        search_query = self.request.GET.get('search')
        search_field = self.request.GET.get('search-field')

        if search_query:
            if search_field == 'all':
                qs = User.objects.filter(
                    Q(profile__about__icontains=search_query) |
                    Q(profile__goals_for_life__icontains=search_query) |
                    Q(profile__interests__icontains=search_query) |
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query)
                )
            if search_field == 'interests':
                qs = User.objects.filter(
                    Q(profile__about__icontains=search_query) |
                    Q(profile__goals_for_life__icontains=search_query) |
                    Q(profile__interests__icontains=search_query)
                )
            if search_field == 'name':
                qs = User.objects.filter(
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query)
                )
            return qs.exclude(id=self.request.user.id)
        return User.objects.filter(is_displayed_in_allies=True).exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        context['search_field'] = self.request.GET.get('search-field')
        return context


class UserUpdateView(LoginRequiredMixin, generic.FormView):
    form_class = UserUpdateForm
    template_name = 'accounts/update_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        page_title = 'Изменить профиль'
        ctx = {
            'page_title': page_title,
            'form': form,
        }
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect(user.get_absolute_url())
        else:
            return self.render_to_response({'form': form})
