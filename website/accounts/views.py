from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
# Create your views here.

def register(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        try:
            user = User.objects.get(username = request.POST['username'])
            return render(request, 'register.html', {'error' : 'Username has a already been taken.'})
        except User.DoesNotExist:
            user = User.objects.create_user(username = request.POST['username'], password = request.POST['password'])
            auth.login(request, user)
            return redirect('board')
    else:
        # User wants to enter info
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('board')
        else:
            return render(request, 'login.html', {'error' : 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('board')
    else:
        return render(request, 'register.html')