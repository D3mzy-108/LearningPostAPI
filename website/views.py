import csv
import json
import os
import datetime
from core.settings import BASE_DIR, STATIC_URL
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'User does not exist.',
            })
        user = get_object_or_404(User, email=email)
        if not user.check_password(password):
            return JsonResponse({
                'success': False,
                'message': 'Incorrect Password.',
            })
        auth.login(request=request, user=user)
        if not user.is_superuser:
            return JsonResponse({
                'success': False,
                'message': 'Account is unauthorized.',
            })
        return JsonResponse({
            'success': True,
            'message': f'Welcome {user.username}.',
            'user': {
                'username': user.username,
                'email': user.email,
                'lastLogin': datetime.datetime.strftime(user.last_login, '%d-%m-%Y'),
            },
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.',
        })


def home(request):
    return render(request, 'website/home.html')


def ts_and_cs(request):
    return redirect('https://learningpost.ng/terms-and-conditions')


def pp(request):
    return redirect('https://learningpost.ng/privacy-policy')


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
    return JsonResponse(context)


def logout(request):
    auth.logout(request)
    return redirect('home')
