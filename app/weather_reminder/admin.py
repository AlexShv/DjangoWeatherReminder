from django.contrib import admin
from .models import User, City, Subscription, WeatherData


# Реєстрація моделей
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'first_name', 
        'last_name',
        'password',
        'email',
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'city',
        'period',
        'created_at',
        'updated_at'
    )


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'city',
        'weather',
        'temperature',
        'humidity',
        'air_pressure',
        'wind_speed',
        'updated_at',
    )
    
