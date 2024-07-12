#authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .forms import SignUpForm

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully...')
            return redirect('Dashboard')
        else:
            messages.error(request, 'Try again...')
            return redirect('Login')
    else:
        return render(request, 'auth/Login.html', {})

def logout_user(request):
    # لا نقوم بمسح الجلسة هنا إذا كنت ترغب في الاحتفاظ ببيانات الاتصال

    logout(request)
    messages.success(request, 'You have been logged out...')
    return redirect('Login')

def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Your account has been created successfully, welcome to 1DataCloud')
            return redirect('Dashboard')
        else:
            messages.error(request, 'There is a problem creating the account, please try again...')
            return redirect('register')
    else:
        return render(request, 'auth/Register.html', {'form': form})