# Generated by Django 3.0 on 2021-05-04 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0028_auto_20210503_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_image', models.ImageField(blank=True, null=True, upload_to='hotel_images/')),
                ('hotels', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traveler.Hotels')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traveler.User_Signup')),
            ],
        ),
    ]