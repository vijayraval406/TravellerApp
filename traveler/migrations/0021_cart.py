# Generated by Django 3.0 on 2021-05-02 12:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0020_auto_20210502_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('qty', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('cabs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traveler.Cabs')),
                ('flights', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traveler.Flights')),
                ('hotels', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traveler.Hotels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traveler.User_Signup')),
            ],
        ),
    ]
