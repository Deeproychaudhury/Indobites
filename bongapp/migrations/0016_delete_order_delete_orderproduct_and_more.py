# Generated by Django 4.1.7 on 2023-04-27 14:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bongapp', '0015_alter_booking_day_alter_booking_exp_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderProduct',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='exp_time',
        ),
        migrations.AlterField(
            model_name='booking',
            name='day',
            field=models.DateField(default=datetime.datetime(2023, 4, 27, 20, 22, 47, 581449)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='seats',
            field=models.CharField(choices=[('2', '2'), ('4', '4'), ('10', '10'), ('20', '20'), ('30+(buffet)', '30+(buffet)')], default='2', max_length=100),
        ),
    ]
