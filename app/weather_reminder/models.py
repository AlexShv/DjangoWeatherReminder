import json
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_celery_beat.models import IntervalSchedule, PeriodicTask


# Моделі для бази даних
class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class City(BaseModel):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']


class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    PERIOD_OF_NOTIFICATIONS = [
        (1, '1 hour'),
        (3, '3 hours'),
        (6, '6 hours'),
        (12, '12 hours'),
    ]
    period = models.IntegerField(
        choices=PERIOD_OF_NOTIFICATIONS,
        help_text='Period of notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f'{self.user_id} has been subscribed and period of notifications is {self.period} hour/hours'
            )


class WeatherData(BaseModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    weather = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    air_pressure = models.FloatField()
    wind_speed = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Weather data for {self.city.name}"
    
    class Meta:
        verbose_name_plural = 'WeatherData'


def create_task(subscription):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=subscription.period,
        period=IntervalSchedule.HOURS
    )
    
    task_name = f'Send email to {subscription.user.email} (Subscription ID: {subscription.id})'

    task = PeriodicTask.objects.create(
        name=task_name,
        task='send_email',
        interval=schedule,
        args=json.dumps([subscription.id]),
        start_time=timezone.now()
    )
    task.save()
    return task


def delete_task(subscription):
    task_name = f'Send email to {subscription.user.email} (Subscription ID: {subscription.id})'
    task = PeriodicTask.objects.filter(name=task_name)
    task.delete()
    return


def edit_task(subscription):
    task_name = f'Send email to {subscription.user.email} (Subscription ID: {subscription.id})'
    task = PeriodicTask.objects.get(name=task_name)
    task.delete()
    create_task(subscription)
    return 
