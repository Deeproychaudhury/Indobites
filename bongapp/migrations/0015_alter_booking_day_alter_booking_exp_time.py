# Generated by Django 4.1.7 on 2023-04-19 05:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bongapp', '0014_remove_booking_name2_booking_exp_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='day',
            field=models.DateField(default=datetime.datetime(2023, 4, 19, 10, 44, 35, 844706)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='exp_time',
            field=models.DateField(default=models.DateField(default=datetime.datetime(2023, 4, 19, 10, 44, 35, 844706))),
        ),
    ]
