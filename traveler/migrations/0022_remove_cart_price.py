# Generated by Django 3.0 on 2021-05-02 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0021_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
    ]