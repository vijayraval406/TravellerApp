# Generated by Django 3.0 on 2021-05-10 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0031_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabcart',
            name='qty',
            field=models.IntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='hotelcart',
            name='qty',
            field=models.IntegerField(default=2),
        ),
    ]