# Generated by Django 3.0 on 2021-04-30 11:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0012_flights_flight_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flights',
            name='flight_arrtime',
            field=models.DateTimeField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='flights',
            name='flight_deptime',
            field=models.DateTimeField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
