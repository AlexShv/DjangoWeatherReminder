# Generated by Django 4.2.9 on 2024-03-05 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather_reminder', '0003_alter_weatherdata_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WeatherData',
        ),
    ]
