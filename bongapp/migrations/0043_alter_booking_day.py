# Generated by Django 5.0.2 on 2024-08-05 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bongapp', '0042_remove_product_stripe_price_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='day',
            field=models.DateField(default=datetime.datetime(2024, 8, 5, 18, 11, 25, 796287)),
        ),
    ]
