# Generated by Django 3.1.2 on 2020-10-29 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyMove', '0002_auto_20201029_0155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='easymoveitem',
            name='url',
        ),
        migrations.AlterField(
            model_name='easymoveitem',
            name='imgURL',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
