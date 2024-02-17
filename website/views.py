from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, logout
from django.contrib import auth
from .models import User


def home(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            user = get_object_or_404(User, email=email)
            if user.check_password(password):
                login(request=request, user=user)
                if user.is_superuser:
                    return redirect('quests')
                else:
                    return HttpResponse('<h1>User is Logged In</h1>')
            else:
                return redirect('home')
        else:
            return redirect('home')
    context = {}
    return render(request, 'website/home.html', context)


def about(request):
    return render(request, 'website/about.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
