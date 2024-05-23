import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models


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
    email = models.EmailField(unique=True, null=True, blank=True)
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
