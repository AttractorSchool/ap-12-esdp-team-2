from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.validators import MinValueValidator
from accounts.models import User
from . import models


class ClubForm(forms.ModelForm):

    class Meta:
        model = models.Club
        fields = (
            'name',
            'category',
            'logo',
            'description',
            'email',
            'phone',
            'city',
            'address',
            'whatsapp_link',
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
            'whatsapp_link': forms.TextInput(attrs={'placeholder': '+7757161577'}),
        }


class ClubUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Club
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
        model = models.Club
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


class ClubServiceCreateForm(forms.ModelForm):
    class Meta:
        model = models.ClubService
        fields = (
            'name',
            'description',
            'price',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'description': forms.Textarea(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'price': forms.NumberInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
        }
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control text-center w-50 mx-auto'}))

    
class CreateClubEventForm(forms.ModelForm):
    class Meta:
        model = models.ClubEvent
        exclude = (
            'old_datetime',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'description': forms.Textarea(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'banner': forms.FileInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'location': forms.TextInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
            'start_datetime': forms.DateInput(attrs={'class': 'form-control text-center w-50 mx-auto', 'type': 'date'}),
            'end_datetime': forms.DateInput(attrs={'class': 'form-control text-center w-50 mx-auto', 'type': 'date'}),
            'entry_requirements': forms.Textarea(attrs={'class': 'form-control text-center w-50 mx-auto'}),
        }

    min_age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1', 'class': 'form-control text-center w-50 mx-auto'}),
        min_value=1,
        validators=[MinValueValidator(1)],
        label='Минимальный допустимый возраст'
    )
    max_age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1', 'class': 'form-control text-center w-50 mx-auto'}),
        min_value=1,
        validators=[MinValueValidator(1)],
        label='Максимальный допустимый возраст'
    )
    club = forms.ModelChoiceField(widget=forms.HiddenInput(), required=True, queryset=models.Club.objects.all())


class AddGalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = models.ClubGalleryPhoto
        fields = ('club', 'image')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control text-center w-50 mx-auto'}),
        }
    club = forms.ModelChoiceField(widget=forms.HiddenInput(), required=True, queryset=models.Club.objects.all())

