# Generated by Django 4.2.13 on 2024-07-17 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0012_alter_clubgalleryphoto_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Имя сообщества'),
        ),
    ]