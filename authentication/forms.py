from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2')