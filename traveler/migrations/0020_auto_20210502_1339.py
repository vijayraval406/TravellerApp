# Generated by Django 3.0 on 2021-05-02 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0019_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='hotel',
            new_name='hotels',
        ),
    ]
