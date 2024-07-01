from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _


class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['phone', ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control text-center'}),
        }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control text-center'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control text-center'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True, 'class': "form-control"}),
        label="Номер телефона",
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            'class': "form-control",
            'id': "id_password2",

        }),
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'avatar', 'first_name', 'last_name')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
        }


class VerifyUserForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control text-center'}),
        label="Код подтверждения"
    )
