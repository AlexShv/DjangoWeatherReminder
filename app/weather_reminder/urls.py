from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import  register, sign_in, sign_out, main, MySubscriptionView, SubscriptionsListView


# Визначив маршрути для реєстрації, авторизації, перегляду списку
# підписок, операцій над підписками 
urlpatterns = [
    path('', main, name='main_page'),
    path('register/', register, name='register'),
    path('login/', sign_in, name='sign_in_page'),
    path('logout/', sign_out, name='sign_out_page'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/subscription/', MySubscriptionView.as_view(), name='add_subscripiton'),
    path('api/subscription/<int:subscription_id>/', MySubscriptionView.as_view(), name='subscripiton'),
    path('api/subscriptions/', SubscriptionsListView.as_view(), name='all_subscriptions'),
]   
