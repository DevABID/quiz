from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(required=False)
    college = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'college', 'password1', 'password2')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login
            return redirect('quiz:quiz_list')  # redirect to quizzes page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})