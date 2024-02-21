import csv
import os
from core.settings import BASE_DIR, STATIC_URL
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login
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


def ts_and_cs(request):
    return render(request, 'website/terms_and_conditions.html')


def pp(request):
    return render(request, 'website/privacy_policy.html')


def faq(request):
    tsv_file_path = os.path.join(BASE_DIR, STATIC_URL, 'assets', 'faq.TSV')
    faqs = []

    try:
        with open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsvfile:
            # Create a TSV reader
            tsv_reader = csv.DictReader(tsvfile, delimiter='\t')
            for row in tsv_reader:
                question = row['Question']
                answer = row['Answer']
                faqs.append({
                    'question': question,
                    'answer': answer,
                })
    except:
        pass

    context = {
        'faqs': faqs,
    }
    return render(request, 'website/faq.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')
