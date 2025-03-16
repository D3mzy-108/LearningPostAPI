import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from admin_app.models import Quest, SubscriptionPlan
from website.models import SubAccounts, User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta, datetime


# ========================================================================================================
# AUTH
# ========================================================================================================
@csrf_exempt
def login_endpoint(request):
    if request.method == 'POST':
        # Extract user data from the request
        user_id = request.POST.get('userId')
        email = request.POST.get('email')
        profileUrl = request.POST.get('profileURL')
        # Add other necessary user information

        # Check if the user already exists
        user, created = User.objects.get_or_create(
            username=user_id, defaults={'email': email, 'last_name': ''})

        # If the user is newly created, set additional attributes
        if created:
            user.profile_photo = profileUrl
            user.is_active = False
            # Set other user attributes as needed
            user.save()

        # Login the user
        auth.login(request, user)

        user_profile = {
            'country': user.country,
            'state': user.state,
        }
        context = {
            'success': True,
            'message': 'Login Successful!',
            'isNewUser': not user.is_active,
            'userProfile': user_profile,
        }
        return JsonResponse(context)
    context = {
        'success': False,
        'message': 'Login Failed!'
    }
    return JsonResponse(context)


@csrf_exempt
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.first_name = request.POST.get('displayName')
        user.country = request.POST.get('country')
        user.state = request.POST.get('state')
        user.is_active = True
        user.save()
        return JsonResponse({
            'success': True,
            'message': 'Profile Saved',
        })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request!',
    })


def get_logged_in_user(request, username):
    user = User.objects.filter(username=username)
    user_profile = {
        'country': '',
        'state': '',
    }
    if user.exists():
        m_user = get_object_or_404(User, username=username)
        userid = m_user.username
        display_name = m_user.first_name
        email = m_user.email
        profile_url = m_user.profile_photo
        user_profile = {
            'country': m_user.country,
            'state': m_user.state,
        }
        sub_accounts = []
        for account in SubAccounts.objects.filter(parent__pk=m_user.pk):
            sub_accounts.append({
                'profileURL': account.child.profile_photo,
                'displayName': account.child.first_name,
                'username': account.child.username,
            })
    else:
        userid = None
        display_name = 'Guest User'
        email = None
        profile_url = ''
        sub_accounts = []
    context = {
        'userId': userid,
        'displayName': display_name,
        'email': email,
        'profileURL': profile_url,
        'userProfile': user_profile,
        'sub_accounts': sub_accounts,
    }
    return JsonResponse(context)


@csrf_exempt
def add_sub_account(request, username):
    if request.method == 'POST':
        code = request.POST.get('username')
        child = get_object_or_404(User, username=code)
        parent = get_object_or_404(User, username=username)
        if not SubAccounts.objects.filter(parent__pk=parent.pk, child__pk=child.pk).exists():
            account_instance = SubAccounts()
            account_instance.parent = parent
            account_instance.child = child
            account_instance.save()
        return JsonResponse({
            'success': True,
            'message': 'Account has been linked!'
        })
    return JsonResponse({
        'success': False,
        'message': 'Invalid Request!'
    })
