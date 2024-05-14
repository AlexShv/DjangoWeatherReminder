from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, CharField, TextInput, PasswordInput


# Форма для реєстрації
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


# Форма для авторизації
class LoginForm(Form):
    email = CharField(
        max_length=65,
        widget=TextInput()
    )
    password = CharField(
        max_length=65,
        label='Password',
        widget=PasswordInput()
    )
