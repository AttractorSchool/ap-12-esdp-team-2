# Generated by Django 4.2.13 on 2024-05-31 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0009_alter_clubjoinrequest_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clubserviceimage',
            old_name='club',
            new_name='service',
        ),
    ]