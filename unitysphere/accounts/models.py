import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.urls import reverse


phone_regex_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть введен в формате: '+999999999'. Максимум 15 чисел."
    )


class User(AbstractUser):
    """
    Модель представляет пользователя приложения.

    Attributes:
        id (UUIDField): Уникальный идентификатор пользователя (автоматически генерируется).
        avatar (ImageField): Фото профиля пользователя.
        phone (CharField): Номер телефона пользователя.
        email (EmailField): Email пользователя.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    avatar = models.ImageField(
        upload_to="user/avatars/",
        default='user/avatars/user.png',
        blank=True,
        verbose_name='Фото',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Номер телефона",
        validators=[phone_regex_validator]
    )
    email = models.EmailField(unique=True, null=True)
    is_displayed_in_allies = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'phone'

    def __str__(self):
        """
        Возвращает строковое представление пользователя.
        """
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.phone

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_formatted_phone(self):
        return self.phone.split('+')[1]

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        super().save(*args, **kwargs)


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        'accounts.User',
        verbose_name='Пользователь',
        related_name='profile',
        on_delete=models.CASCADE
    )
    about = models.TextField(null=True, blank=True, verbose_name='О себе')
    goals_for_life = models.TextField(null=True, blank=True, verbose_name='Цели на жизнь')
    interests = models.TextField(null=True, blank=True, verbose_name='Интересы')