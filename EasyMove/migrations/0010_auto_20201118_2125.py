# Generated by Django 3.1.2 on 2020-11-18 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EasyMove', '0009_auto_20201118_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyMove.easymoveitem'),
        ),
    ]