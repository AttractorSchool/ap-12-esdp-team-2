import uuid

from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.db import models
from accounts.models import phone_regex_validator


class ClubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iata_code = models.CharField(max_length=20, db_index=True, verbose_name='Код города')
    name = models.CharField(max_length=50, verbose_name='Название города')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    category = models.ForeignKey(
        'clubs.ClubCategory',
        on_delete=models.SET_NULL,
        related_name='clubs',
        null=True,
        verbose_name='Категория',
        limit_choices_to={'is_active': True},
    )
    logo = models.ImageField(
        upload_to='club/logos',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        default='club/logos/club-icon.png',
    )
    managers = models.ManyToManyField(
        'accounts.User',
        related_name='co_managed_clubs',
        blank=True,
        verbose_name='Соуправляющие клуба',
    )
    description = models.TextField(validators=[MinLengthValidator(200)], verbose_name='Описание')
    email = models.EmailField(verbose_name='Контактный email')
    phone = models.CharField(validators=[phone_regex_validator], verbose_name='Контактный телефон', max_length=20)
    city = models.ForeignKey(
        to='clubs.City', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Город'
    )
    address = models.CharField(default='No location', verbose_name='Локация клуба', max_length=150, blank=True)
    members = models.ManyToManyField(
        'accounts.User',
        verbose_name='Члены клуба',
        related_name='members_of_clubs',
        blank=True,
    )
    likes = models.ManyToManyField(
        'accounts.User',
        related_name='liked_by_users',
        blank=True,
        verbose_name='Нравится'
    )
    likes_count = models.PositiveIntegerField(default=0,)
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    subscribers = models.ManyToManyField(
        'self', related_name='subscriptions', symmetrical=False, verbose_name='Подписчики'
    )
    subscribers_count = models.PositiveIntegerField(default=0, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'


class ClubService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Клуб',
        limit_choices_to={'is_active': True},
    )
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга клуба'
        verbose_name_plural = 'Услуги клуба'


class Ads(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name='Название рекламы')
    description = models.TextField(verbose_name='Описание', max_length=1000)
    ads_img = models.ImageField(
        upload_to='ads',
        verbose_name='Изображение',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, verbose_name='Клуб',
        limit_choices_to={'is_active': True},
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'
        ordering = ['-created_at']


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name='Название мероприятия')
    description = models.TextField(verbose_name='Описание', validators=[MinLengthValidator(100)])
    event_img = models.ImageField(
        upload_to='events', verbose_name='Изображение мероприятия',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    club = models.ForeignKey(
        'clubs.Club', on_delete=models.CASCADE, related_name='events',
        verbose_name='Клуб', limit_choices_to={'is_active': True},
    )
    event_date = models.DateField(verbose_name='Дата мероприятия')
    old_event_date = models.DateField(verbose_name='Старая дата мероприятия', null=True, blank=True)
    min_age = models.PositiveIntegerField(verbose_name='Минимальный возраст', default=0)
    location = models.CharField(max_length=255, verbose_name='Местоположение', null=True, blank=True)
    other_conditions = models.TextField(verbose_name='Другие условия', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-created_at']
