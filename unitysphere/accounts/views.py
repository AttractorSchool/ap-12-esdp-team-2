from django.shortcuts import render
from django.views import generic

from accounts.forms import RegisterUserForm


class RegisterUserView(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register_user.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Регистрация'
        return ctx
