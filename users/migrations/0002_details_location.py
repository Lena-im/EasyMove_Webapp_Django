# Generated by Django 3.1.2 on 2020-11-18 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='location',
            field=models.CharField(default='VA', max_length=50),
        ),
    ]
