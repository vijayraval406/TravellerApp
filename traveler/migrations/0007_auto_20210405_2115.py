# Generated by Django 3.0 on 2021-04-05 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0006_auto_20210405_2112'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bus',
        ),
        migrations.DeleteModel(
            name='Cabs',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.DeleteModel(
            name='Hotels',
        ),
        migrations.DeleteModel(
            name='Trains',
        ),
    ]
