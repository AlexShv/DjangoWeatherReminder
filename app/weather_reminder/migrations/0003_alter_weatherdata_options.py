# Generated by Django 4.2.9 on 2024-03-05 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather_reminder', '0002_weatherdata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weatherdata',
            options={'verbose_name_plural': 'WeatherData'},
        ),
    ]