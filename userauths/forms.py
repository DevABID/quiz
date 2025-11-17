from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(required=False, label='Full Name')
    college = forms.CharField(required=False, label='College')

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'college', 'password1', 'password2')
