# Generated by Django 4.2.13 on 2024-05-27 10:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_alter_clubads_options_alter_festival_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='festival',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 15, 32, 25, 393323), verbose_name='Дата начала'),
            preserve_default=False,
        ),
    ]
