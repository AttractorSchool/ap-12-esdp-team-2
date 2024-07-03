from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
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
            user = form.save()
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        success_url = self.request.META.get('HTTP_REFERER', '/')
        return success_url


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


class UserUpdateView(LoginRequiredMixin, generic.FormView):
    form_class = UserUpdateForm
    template_name = 'accounts/update_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        page_title = 'Изменить профиль'
        categories = ClubCategory.objects.all()
        ctx = {
            'page_title': page_title,
            'categories': categories,
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
