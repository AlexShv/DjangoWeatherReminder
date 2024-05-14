from rest_framework import serializers
from .models import Subscription, City


# Серіалізатор для міст
class CityInSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name', )


 # Серіалізатор для підписок
class SubscriptionSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    city = CityInSubscriptionSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ('subscription_id', 'user_email', 'period', 'city')
        extra_kwargs = {'subscription_id': {'source': 'id'}}
