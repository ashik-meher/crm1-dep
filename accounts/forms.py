from django import forms
from django.forms import ModelForm
from .models import Order, Customer

# user creation

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
