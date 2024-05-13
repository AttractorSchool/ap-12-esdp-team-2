import uuid

from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.db import models
from accounts.models import phone_regex_validator
from pytils.translit import slugify


class ClubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iata_coe = models.CharField(db_index=True, max_length=20, unique=True, verbose_name='Код города')
    name = models.CharField(max_length=20, unique=True, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя клуба')
    category = models.ForeignKey(
        'clubs.ClubCategory',
        on_delete=models.SET_NULL,
        related_name='clubs',
        null=True,
        verbose_name='Категория клуба'
    )
    logo = models.ImageField(
        upload_to='club/logos',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        default='club/logos/club-icon.png',
        verbose_name='Логотип'
    )
    managers = models.ManyToManyField(
        'accounts.User',
        related_name='co_managed_clubs',
        blank=True,
        verbose_name='Соуправляющие клуба'
    )
    description = models.TextField(validators=[MinLengthValidator(200)], verbose_name='Описание')
    email = models.EmailField(verbose_name='Контактный email')
    phone = models.CharField(validators=[phone_regex_validator], verbose_name='Контактный телефон', max_length=20)
    city = models.ForeignKey(
        to='clubs.City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clubs',
        verbose_name='Город'
    )
    address = models.CharField(default='No location', verbose_name='Локация клуба', max_length=150, blank=True)
    members = models.ManyToManyField(
        'accounts.User',
        verbose_name='Члены клуба',
        related_name='member_of_clubs',
        blank=True,
    )
    likes = models.ManyToManyField(
        to='accounts.User',
        verbose_name='Лайкнули',
        related_name='liked_by_users',
        blank=True,
    )
    partners = models.ManyToManyField(
        to='self',
        verbose_name='Клубы-партнеры',
        related_name='club_partners',
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'


class ClubGalleryPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    club = models.ForeignKey(
        to='clubs.Club',
        on_delete=models.CASCADE,
        related_name='gallery_photos',
        verbose_name='Клуб'
    )
    image = models.ImageField(upload_to='clubs/gallery', verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.club.name}-{self.image.name}'

    class Meta:
        verbose_name = "Фотогалерея"
        verbose_name_plural = "Фотогалерея"


class ClubEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    club = models.ForeignKey(
        to='clubs.Club',
        on_delete=models.CASCADE,
        related_name='club_events',
        verbose_name='Клуб'
    )
    title = models.CharField(max_length=150, verbose_name='Название события')
    description = models.TextField(verbose_name='Описание')
    banner = models.ImageField(upload_to='clubs/event_banners', verbose_name='Баннер события')
    location = models.CharField(max_length=150, verbose_name='Место проведения')
    start_datetime = models.DateTimeField(verbose_name='Дата и время начала')
    old_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(verbose_name='Дата и время завершения')
    min_age = models.PositiveIntegerField(blank=True, null=True, verbose_name='Минимальный возврат для входа')
    max_age = models.PositiveIntegerField(blank=True, null=True, verbose_name='Максимальный возврат для входа')
    entry_requirements = models.TextField(blank=True, null=True, verbose_name='Требования для входа')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "События"
        verbose_name_plural = "События"


class ClubAds(models.Model):
    AD_TYPES_CHOICES = (
        ('Акция', 'Акция'),
        ('Приглашение', 'Приглашение'),
        ('Новости', 'Новости'),
        ('Покупка', 'Покупка'),
        ('Продажа', 'Продажа'),
        ('Другое', 'Другое'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    club = models.ForeignKey(
        to='clubs.Club',
        on_delete=models.CASCADE,
        related_name='club_ads',
        verbose_name='Клуб'
    )
    type = models.CharField(max_length=20, choices=AD_TYPES_CHOICES)
    title = models.CharField(max_length=150, verbose_name='Название события')
    description = models.TextField(verbose_name='Описание')
    img = models.ImageField(upload_to='clubs/ad_photos', verbose_name='Фото объявления')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявления'
        verbose_name_plural = 'Объявления'
#dfsdfsdfsdfsdf