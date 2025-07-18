import datetime
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from admin_app.models import UserFeedback
from endpoints.api_views.subscription import is_subscription_valid
from website.models import User, UserSubscription
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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
        user_subscriptions = UserSubscription.objects.filter(
            profile__email=email)
        if not user_subscriptions.exists():
            user_subscription = UserSubscription()
            today = datetime.date.today()
            expiry_date = today + datetime.timedelta(days=7)
            user_subscription.expiry_date = expiry_date
            user_subscription.is_confirmed = True
            user_subscription.profile = user
            user_subscription.save()

        user_profile = {
            'country': user.country,
            'state': user.state,
            'dob': user.dob.strftime('%d-%m-%Y') if user.dob else None,
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
@require_POST
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    user.first_name = request.POST.get('displayName')
    user.country = request.POST.get('country')
    user.state = request.POST.get('state')
    user.dob = datetime.datetime.strptime(request.POST.get('dob'), '%d-%m-%Y')
    user.is_active = True
    user.save()
    return JsonResponse({
        'success': True,
        'message': 'Profile Saved',
    })


def get_logged_in_user(request, username):
    user = User.objects.filter(username=username)
    user_profile = {
        'country': '',
        'state': '',
        'dob': '',
    }
    is_subscribed = False
    if user.exists():
        m_user = get_object_or_404(User, username=username)
        is_subscribed = is_subscription_valid(user=m_user)
        userid = m_user.username
        display_name = m_user.first_name
        email = m_user.email
        profile_url = m_user.profile_photo
        user_profile = {
            'country': m_user.country,
            'state': m_user.state,
            'dob': m_user.dob.strftime('%d-%m-%Y') if m_user.dob else None,
        }
        friends = []
        for account in m_user.friends.all():
            friends.append({
                'profileURL': account.profile_photo,
                'displayName': account.first_name,
                'username': account.username,
            })
    else:
        userid = None
        display_name = 'Guest User'
        email = None
        profile_url = ''
        friends = []
    context = {
        'userId': userid,
        'displayName': display_name,
        'email': email,
        'profileURL': profile_url,
        'userProfile': user_profile,
        'friends': friends,
        'is_subscribed': is_subscribed,
    }
    return JsonResponse(context)


# ========================================================================================================
# FRIENDS
# ========================================================================================================
@csrf_exempt
def add_friend(request, username):
    if request.method == 'POST':
        code = request.POST.get('ref_code')
        party_a = get_object_or_404(User, username=username)
        party_b = get_object_or_404(User, username=code)
        if not party_a.friends.all().filter(pk=party_b.pk).exists():
            party_a.friends.add(party_b)
            party_b.friends.add(party_a)
            party_a.save()
            party_b.save()
        return JsonResponse({
            'success': True,
            'message': 'Account has been linked!'
        })
    return JsonResponse({
        'success': False,
        'message': 'Invalid Request!'
    })


@require_POST
@csrf_exempt
def update_status(request):
    username = request.POST.get('username') or ''
    is_online = request.POST.get('is_online') or False
    user = get_object_or_404(User, username=username)
    user.online = is_online
    user.save()
    status = "online" if is_online else "offline"
    return JsonResponse({
        'success': True,
        'message': f'{user.first_name} is {status}',
    })


# ========================================================================================================
# DELETE
# ========================================================================================================
@require_POST
@csrf_exempt
def request_account_deletion(request):
    data = json.loads(request.body)
    email = data.get('email')
    user_display_name = data.get('user_display_name')
    reason = data.get('reason')
    print(reason)
    print(email)

    if User.objects.filter(email=email, first_name=user_display_name).exists():
        user = User.objects.get(email=email)
        feedback_instance = UserFeedback()
        feedback_instance.feedback_type = 'unsatisfied_user'
        feedback_instance.message = f'Account was deleted because: \n{reason}'
        feedback_instance.save()
        user.delete()
        return JsonResponse({
            'success': True,
            'message': 'Account has been deleted.',
        })
    return JsonResponse({
        'success': False,
        'message': 'User with the provided credentials does not exist.',
    })
