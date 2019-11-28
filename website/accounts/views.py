from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        try:
            user = User.objects.get(username = request.POST['username'])
            return render(request, 'register.html', {'error' : '해당 ID로는 회원가입 할 수 없습니다. 사용자가 이미 존재합니다.'})
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
            return render(request, 'login.html', {'error' : 'ID나 비밀번호가 틀립니다.'})
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('board')
    else:
        return render(request, 'register.html')

def info(request, username):
    user = User.objects.get(username = username)
    return render(request, 'info.html', {'person' : user})

def changeInfo(request):
    context = {}

    #if request.method == 'GET':
        # change Username
        # new_username = request.GET.get('new_username')
        # user = request.user
        # user.username = new_username
        # user.save()
        #return redirect('board')

    if request.method == 'POST':
        # change Password
        current_password = request.POST['origin_password']
        user = request.user
        if check_password(current_password, user.password):
            if request.POST['new_password1'] == request.POST['new_password2']:
                new_password = request.POST['new_password1']
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                return redirect('board')
            else:
                context.update({'error' : "변경 비밀번호가 일치하지 않습니다."})
        else:
            context.update({'error' : "현재 비밀번호가 일치하지 않습니다."})
    return render(request, 'changeInfo.html', context)

@login_required
def deleteMe(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('login')