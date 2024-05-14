import requests
from .models import WeatherData, City
from django.utils import timezone
from decouple import config


# Переводжу градуси з Кельвіну в Цельсій
def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius


# Функція для отримання погоди, якщо інформація про погоду була
# оновлена в останні 2 години, то буде повертатися інформація з бази даних
# інакше - буде виконуватися новий запит на отримання погоди та оновлення в баз даних
def get_weather_info(required_town):
    city_instance, created = City.objects.get_or_create(name=required_town)
    weather_data = WeatherData.objects.filter(city=city_instance).first()
    if weather_data and (timezone.now() - weather_data.updated_at).seconds < 7200:
        return {
            'weather': weather_data.weather,
            'temperature': weather_data.temperature,
            'humidity': weather_data.humidity,
            'air_pressure': weather_data.air_pressure,
            'wind_speed': weather_data.wind_speed
        }
    else:
        data = requests.get(
            'https://api.openweathermap.org/data/2.5/weather', 
            params={'q': required_town, 'appid': config('API_KEY')}
        )

        extracted_data = {
            'weather': data.json()['weather'][0]['description'],
            'temperature': kelvin_to_celsius(data.json()['main']['temp']),
            'humidity': data.json()['main']['humidity'],
            'air_pressure': data.json()['main']['pressure'],
            'wind_speed': data.json()['wind']['speed']
        }

        WeatherData.objects.update_or_create(
            city=city_instance,
            defaults=extracted_data
        )

        return extracted_data
