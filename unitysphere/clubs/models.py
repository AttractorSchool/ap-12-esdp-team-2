from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.db import models
from accounts.models import phone_regex_validator
from pytils.translit import slugify


class ClubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    category = models.ForeignKey(
        'webapp.ClubCategory',
        on_delete=models.SET_NULL,
        related_name='clubs',
        null=True,
    )
    logo = models.ImageField(
        upload_to='club/logos',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        default='club/logos/club-icon.png',
    )
    manager = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='managed_clubs',
        verbose_name='Управляющий клуба',
    )
    co_managers = models.ManyToManyField(
        'accounts.User',
        related_name='co_managed_clubs',
        blank=True,
        verbose_name="Соуправляющие клуба"
    )
    description = models.TextField(validators=[MinLengthValidator(200)], verbose_name="Описание")
    email = models.EmailField(verbose_name="Контактный email")
    phone = models.CharField(validators=[phone_regex_validator], verbose_name="Контактный телефон", max_length=20)
    city = models.ForeignKey(to='clubs.City', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(default="No location", verbose_name="Локация клуба", max_length=150, blank=True)
    members = models.ManyToManyField(
        'accounts.User',
        verbose_name="Члены клуба",
        related_name='clubs',
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'


