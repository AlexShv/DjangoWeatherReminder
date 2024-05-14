from celery import shared_task
from .extract_weather import get_weather_info
from django.core.mail import EmailMessage
from .models import Subscription
from django.utils import timezone
from math import gcd
from functools import reduce


# Задача для відправлення повідомлення
@shared_task(name='send_email')
def send_weather_updates(subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    user = subscription.user
    
    unique_periods = Subscription.objects.filter(user=user).values('period').distinct()
    
    # Знаходимо найменше спільне кратне для всіх періодів
    lcm = reduce(lambda x, y: x * y // gcd(x, y), [period['period'] for period in unique_periods])

    # Перевіряємо, чи пройшов достатній час для відправки листа зі зведеною інформацією
    if lcm == 1 or (timezone.now().hour % lcm) == 0:
        message = ""

        for period in unique_periods:
            subscriptions = Subscription.objects.filter(user=user, period=period['period'])

            for subscription in subscriptions:
                city_name = subscription.city.name
                weather_data = get_weather_info(city_name)

                message += f'''Weather update for {city_name}:
                    General information: {weather_data['weather']},
                    Temperature: {weather_data['temperature']:.1f}°C,
                    Humidity: {weather_data['humidity']}%,
                    Air Pressure: {weather_data['air_pressure']} hPa,
                    Wind Speed: {weather_data['wind_speed']} m/s
                \n'''

        if message:
            email_subject = f"Weather Update for {user.first_name} {user.last_name}"
            email = EmailMessage(subject=email_subject, body=message, to=[user.email])
            email.send()
            