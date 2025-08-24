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
            response = redirect('login')
            response.set_cookie('login_status', 'logged_in',
                                max_age=3600, httponly=True, samesite='Lax')
            messages.success(request, 'login succesfully')
            return response

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')



