# Generated by Django 3.0 on 2021-05-01 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0017_auto_20210501_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotels',
            name='hotel_chkin',
        ),
        migrations.RemoveField(
            model_name='hotels',
            name='hotel_chkout',
        ),
        migrations.RemoveField(
            model_name='hotels',
            name='hotel_dest_image',
        ),
    ]
