# Generated by Django 5.0.2 on 2024-08-01 15:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bongapp', '0022_alter_booking_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='day',
            field=models.DateField(default=datetime.datetime(2024, 8, 1, 20, 47, 55, 662279)),
        ),
    ]