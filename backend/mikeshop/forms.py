from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import User
from django.db import transaction

class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user
    
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password'}))

from .models import *

class OrderForm(ModelForm):
    shipping_addr = forms.CharField(label="Shipping Address",widget=forms.TextInput(attrs={'class': "aesthetic-windows-95-text-input", 'placeholder': 'Shipping address', 'id': 'ship-addr'}))
    class Meta:
        model = Order
        fields = ['shipping_addr']

from .models import Feedback
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = []