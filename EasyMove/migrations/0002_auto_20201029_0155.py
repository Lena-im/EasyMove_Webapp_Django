# Generated by Django 3.1.2 on 2020-10-29 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EasyMove', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='easymoveitem',
            old_name='data_posted',
            new_name='date_posted',
        ),
    ]
