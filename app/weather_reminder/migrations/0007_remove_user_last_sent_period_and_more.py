# Generated by Django 4.2.9 on 2024-03-06 11:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('weather_reminder', '0006_user_last_sent_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_sent_period',
        ),
        migrations.AddField(
            model_name='subscription',
            name='last_sent_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]