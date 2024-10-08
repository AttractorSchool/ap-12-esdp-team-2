# Generated by Django 4.2.13 on 2024-09-04 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_serviceforclubs_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceforclubs',
            name='price',
        ),
        migrations.AddField(
            model_name='serviceforclubs',
            name='max_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена до(KZT.)'),
        ),
        migrations.AddField(
            model_name='serviceforclubs',
            name='min_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена от(KZT.)'),
        ),
    ]
