# Generated by Django 4.2.9 on 2024-03-05 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather_reminder', '0004_delete_weatherdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weather', models.CharField(max_length=255)),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('air_pressure', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather_reminder.city')),
            ],
            options={
                'verbose_name_plural': 'WeatherData',
            },
        ),
    ]
