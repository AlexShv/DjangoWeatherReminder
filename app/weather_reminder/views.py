from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Subscription, City, create_task, edit_task, delete_task
from rest_framework.permissions import IsAuthenticated
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import  SubscriptionSerializer
from rest_framework import status
from rest_framework.generics import ListAPIView


# Функція представлення для реєєстрації
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, 'Registration Successful')
            return redirect('main_page')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form, 'title': 'Register'})


# Для авторизації
def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('main_page')

        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'title': 'Login'})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('main_page')

        return render(request, 'login.html', {'form': form, 'title': 'Login'})


# Для виходу з акаунту
def sign_out(request):
    logout(request)
    return render(request, 'logout.html', {'title': 'Logout'})


# Головна сторінка сайту
@login_required
def main(request):
    return render(request, 'main.html', {'title': 'Homepage'})


# Клас для операцій над підписками:
# створення, редагування, отримання та видалення певної підписки
class MySubscriptionView(APIView):

    def get(self, request, subscription_id):
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=request.user)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response('Subscription does not exists')

    def post(self, request):
        new_subscriptions = []

        for data in request.data:
            city_name = data.get('city')

            try:
                city = City.objects.get(name=city_name)
            except City.DoesNotExist:
                city = City.objects.create(name=city_name)

            new_subscription = Subscription.objects.create(
                user=request.user,
                city=city,
                period=data.get('period')
            )
            new_subscriptions.append(new_subscription)
            create_task(new_subscription)

        serializer = SubscriptionSerializer(new_subscriptions, many=True) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, subscription_id):
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=request.user)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

        for data in request.data:
            period = data.get('period')
            input_city = data.get('city')

            try:
                city = City.objects.get(name=input_city)
            except City.DoesNotExist:
                city = City.objects.create(name=input_city)

            subscription.period = period
            subscription.city = city
            subscription.save()
            edit_task(subscription)

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def delete(self, request, subscription_id):
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=request.user)
            delete_task(subscription)
            subscription.delete()

            return Response('Subscriptions have been deleted')
        except Subscription.DoesNotExist:
            return Response('Subscription not found')
        

# Для перегляду усіх створених підписок
class SubscriptionsListView(ListAPIView):
    serializer_class =  SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
