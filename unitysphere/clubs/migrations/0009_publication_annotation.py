# Generated by Django 4.2.13 on 2024-09-09 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0008_publication_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='annotation',
            field=models.TextField(default='asd', verbose_name='Краткое содержание'),
            preserve_default=False,
        ),
    ]