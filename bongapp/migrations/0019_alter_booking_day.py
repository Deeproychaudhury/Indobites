# Generated by Django 5.0.2 on 2024-07-31 14:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bongapp', '0018_alter_booking_day_ordermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='day',
            field=models.DateField(default=datetime.datetime(2024, 7, 31, 19, 34, 10, 425005)),
        ),
    ]