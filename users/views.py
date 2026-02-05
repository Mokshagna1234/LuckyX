from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile




def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
        messages.error(request, 'Invalid credentials')

    return render(request, 'auth/login.html') 


def logout_view(request):
    logout(request)
    return redirect('/login/')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'auth/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'auth/signup.html')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, 'auth/signup.html') 


@login_required
def account_page(request):
    return render(request, 'account.html')

@login_required
def account_page(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'account.html', {
        'profile': profile
    })

@login_required
def account_details(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'account_details.html', {
        'profile': profile
    })

