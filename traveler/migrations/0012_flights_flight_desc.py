# Generated by Django 3.0 on 2021-04-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0011_flights_flight_dest_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='flights',
            name='flight_desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]