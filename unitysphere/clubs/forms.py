from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from accounts.models import User
from .models import Club


class ClubForm(forms.ModelForm):

    class Meta:
        model = Club
        fields = (
            'name',
            'category',
            'logo',
            'description',
            'email',
            'phone',
            'city',
            'address',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'category': forms.Select(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'logo': forms.FileInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'description': forms.Textarea(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'phone': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'city': forms.Select(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'address': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
        }


class ClubUpdateForm(forms.ModelForm):

    class Meta:
        model = Club
        exclude = (
            'creater',
            'members',
            'members_count',
            'managers',
            'likes_count',
            'is_private',
            'is_active',
            'likes',
            'partners',
            'partners_count'
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'category': forms.Select(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'logo': forms.FileInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'description': forms.Textarea(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'phone': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'city': forms.Select(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'address': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
        }


class SelectClubManagersForm(forms.ModelForm):

    managers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=FilteredSelectMultiple(
            attrs={'class': 'form-control'},
            is_stacked=False,
            verbose_name='',
        ),
        required=False,
        label='Управляющие клуба'
    )

    class Meta:
        model = Club
        fields = ['managers',]

    class Media:
        css = {
            'all': ('/static/admin/css/widgets.css',),
        }
        js = ('/admin/jsi18n',)

    def clean_choised_users(self):
        choiced_users = self.cleaned_data['managers']
        return choiced_users

    @staticmethod
    def required_at_least_one_manager(users_after, form):
        if len(users_after) == 0:
            form.add_error('managers', 'У клуба должен быть хотя бы один менеджер')
            return False
        return True
