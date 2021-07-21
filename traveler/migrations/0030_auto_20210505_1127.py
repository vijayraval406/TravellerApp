# Generated by Django 3.0 on 2021-05-05 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0029_hotelgallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelgallery',
            name='hotel_image',
            field=models.ImageField(blank=True, null=True, upload_to='hotel_gallery/'),
        ),
        migrations.AlterField(
            model_name='hotels',
            name='hotel_name',
            field=models.CharField(choices=[('The Paradise Inn', 'The Paradise Inn'), ('Hotel deLuxe', 'Hotel deLuxe'), ('Four Seasons', 'Four Seasons'), ('Hi-Way Inn', 'Hi-Way Inn'), ('Candlewood Suites', 'Candlewood Suites'), ('Cute Mountains', 'Cute Mountains.'), ('Hotel Bliss', 'Hotel Bliss')], max_length=100),
        ),
    ]
