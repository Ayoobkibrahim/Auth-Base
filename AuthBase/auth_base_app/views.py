from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


@csrf_protect
@never_cache
def Loginview(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return redirect('login')

        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            response = redirect('home')
            response.set_cookie('login_status', 'logged_in',
                                max_age=3600, httponly=True, samesite='Lax')
            messages.success(request, 'login succesfully')
            return response

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


@csrf_protect
@never_cache
def signupView(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')

        if password != confirmPassword:
            messages.error(request, 'Password donot match')
            return redirect('signup')

        if not username or not password or not confirmPassword:
            messages.error(request, 'All fields are required')
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, 'username must be alphanumirc')
            return redirect('signup')

        if len(password) < 8:
            messages.error(
                request, 'Password must be at least 8 characters long')
            return redirect('signup')

        user = User.objects.create_user(
            username=username, password=password)

        messages.success(request, 'Signup succesfull. Please Login')
        return redirect('login')
    return render(request, 'signup.html')


@login_required(login_url='login')
@never_cache
def homeView(request):
    username = request.session.get('username', 'Guest')
    return render(request, 'home.html', {'username': username})


def logoutView(request):
    logout(request)
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('login_status')
    messages.success(request, "You have been logged out successfully.")
    return response
