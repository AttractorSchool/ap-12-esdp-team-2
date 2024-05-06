from django.views import generic
from .forms import RegisterUserForm, UserLoginForm


class RegisterUserView(generic.FormView):
    form_class = RegisterUserForm
    template_name = 'accounts/register_user.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Центр сообществ - Регистрация'
        return ctx


class LoginUserView(generic.FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login_user.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Центр сообществ - Вход'
        return ctx
