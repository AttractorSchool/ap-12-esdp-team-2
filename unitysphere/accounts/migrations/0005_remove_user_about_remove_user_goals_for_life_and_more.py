# Generated by Django 4.2.13 on 2024-06-27 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_interests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='about',
        ),
        migrations.RemoveField(
            model_name='user',
            name='goals_for_life',
        ),
        migrations.RemoveField(
            model_name='user',
            name='interests',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('about', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('goals_for_life', models.TextField(blank=True, null=True, verbose_name='Цели на жизнь')),
                ('interests', models.TextField(blank=True, null=True, verbose_name='Интересы')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
