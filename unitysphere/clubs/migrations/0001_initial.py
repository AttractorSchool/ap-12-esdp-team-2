# Generated by Django 4.2.13 on 2024-05-13 12:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('iata_coe', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='Код города')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Имя')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Имя клуба')),
                ('logo', models.ImageField(default='club/logos/club-icon.png', upload_to='club/logos', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Логотип')),
                ('description', models.TextField(validators=[django.core.validators.MinLengthValidator(200)], verbose_name='Описание')),
                ('email', models.EmailField(max_length=254, verbose_name='Контактный email')),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть введен в формате: '+999999999'. Максимум 15 чисел.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Контактный телефон')),
                ('address', models.CharField(blank=True, default='No location', max_length=150, verbose_name='Локация клуба')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Клуб',
                'verbose_name_plural': 'Клубы',
            },
        ),
        migrations.CreateModel(
            name='ClubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='ClubGalleryPhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='clubs/gallery', verbose_name='Фото')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_photos', to='clubs.club', verbose_name='Клуб')),
            ],
        ),
        migrations.CreateModel(
            name='ClubEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='Название события')),
                ('description', models.TextField(verbose_name='Описание')),
                ('banner', models.ImageField(upload_to='clubs/event_banners', verbose_name='Баннер события')),
                ('location', models.CharField(max_length=150, verbose_name='Место проведения')),
                ('start_datetime', models.DateTimeField(verbose_name='Дата и время начала')),
                ('old_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(verbose_name='Дата и время завершения')),
                ('min_age', models.IntegerField(blank=True, null=True, verbose_name='Минимальный возврат для входа')),
                ('max_age', models.IntegerField(blank=True, null=True, verbose_name='Максимальный возврат для входа')),
                ('entry_requirements', models.TextField(blank=True, null=True, verbose_name='Требования для входа')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club_events', to='clubs.club', verbose_name='Клуб')),
            ],
        ),
        migrations.CreateModel(
            name='ClubAds',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Акция', 'Акция'), ('Приглашение', 'Приглашение'), ('Новости', 'Новости'), ('Покупка', 'Покупка'), ('Продажа', 'Продажа'), ('Другое', 'Другое')], max_length=20)),
                ('title', models.CharField(max_length=150, verbose_name='Название события')),
                ('description', models.TextField(verbose_name='Описание')),
                ('img', models.ImageField(upload_to='clubs/ad_photos', verbose_name='Фото объявления')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club_ads', to='clubs.club', verbose_name='Клуб')),
            ],
        ),
        migrations.AddField(
            model_name='club',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clubs', to='clubs.clubcategory', verbose_name='Категория клуба'),
        ),
        migrations.AddField(
            model_name='club',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clubs', to='clubs.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='club',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_by_users', to=settings.AUTH_USER_MODEL, verbose_name='Лайкнули'),
        ),
        migrations.AddField(
            model_name='club',
            name='managers',
            field=models.ManyToManyField(blank=True, related_name='co_managed_clubs', to=settings.AUTH_USER_MODEL, verbose_name='Соуправляющие клуба'),
        ),
        migrations.AddField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member_of_clubs', to=settings.AUTH_USER_MODEL, verbose_name='Члены клуба'),
        ),
        migrations.AddField(
            model_name='club',
            name='partners',
            field=models.ManyToManyField(blank=True, related_name='club_partners', to='clubs.club', verbose_name='Клубы-партнеры'),
        ),
    ]
