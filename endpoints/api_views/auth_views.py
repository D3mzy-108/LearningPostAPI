import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from admin_app.models import Quest, SubscriptionPlan
from website.models import SubAccounts, SubscriptionLog, User, UserSubscription
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

        if not UserSubscription.objects.filter(profile__pk=user.pk).exists():
            subscription = UserSubscription()
            trial_period = date.today() + timedelta(days=7)
            subscription.expiry_date = trial_period.strftime('%Y-%m-%d')
            grade_list = Quest.objects.all().order_by(
                'grade').values_list('grade', flat=True).distinct()
            list_of_grades = []
            for grade in grade_list:
                list_of_grades.append(grade)
            subscription.supported_grades = (" --- ").join(list_of_grades)
            subscription.profile = user
            subscription.save()
        else:
            subscription = user.subscription
        user_profile = {
            'country': user.country,
            'state': user.state,
        }
        user_subscription = {
            'expiry_date': subscription.expiry_date,
            'support_quest': subscription.support_quest,
            'support_bookee': subscription.support_bookee,
            'support_akada': subscription.support_akada,
            'supported_grades': subscription.supported_grades.split(' --- '),
        }
        context = {
            'success': True,
            'message': 'Login Successful!',
            'isNewUser': not user.is_active,
            'userProfile': user_profile,
            'subscription': user_subscription,
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
        if not UserSubscription.objects.filter(profile__pk=user.pk).exists():
            subscription = UserSubscription()
            trial_period = date.today() + timedelta(days=7)
            subscription.expiry_date = trial_period.strftime('%Y-%m-%d')
            subscription.profile = user
            subscription.save()
        else:
            subscription = user.subscription
        return JsonResponse({
            'success': True,
            'message': 'Profile Saved',
            'user_subscription': {
                'expiry_date': subscription.expiry_date,
                'support_quest': subscription.support_quest,
                'support_bookee': subscription.support_bookee,
                'support_akada': subscription.support_akada,
                'supported_grades': subscription.supported_grades.split(' --- '),
            },
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


def get_plans(request):
    plans = SubscriptionPlan.objects.all()
    plan_list = []
    for plan in plans:
        plan_list.append({
            'plan': plan.plan,
            'duration': plan.duration,
            'quest_cost': plan.quest_price,
            'bookee_cost': plan.bookee_price,
            'akada_cost': plan.akada_price,
        })

    context = {
        'success': True,
        'plans': plan_list,
        'sign': '₦',
    }
    return JsonResponse(context)


def log_subscription(request):
    username = request.GET.get('username')
    amount = request.GET.get('amount')
    currency = request.GET.get('currency')
    sdate = datetime.now()
    code = f'LearningPostSubscription-{sdate.year}{sdate.month}{sdate.day}-{sdate.time()}'
    user = get_object_or_404(User, username=username)
    if amount is not None and currency is not None:
        subscription_log = SubscriptionLog()
        subscription_log.user = user
        subscription_log.amount = amount
        subscription_log.code = code
        subscription_log.currency = currency
        subscription_log.save()
        return JsonResponse({
            'success': True,
            'code': subscription_log.code,
            'user': {
                'username': user.username,
                'name': user.first_name,
                'email': user.email,
                'phone': user.phone,
            },
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Required parameters not met!'
        })


def subscription_success(request, username, quest_support, bookee_support, akada_support, selected_grades, duration):
    user = get_object_or_404(User, username=username)
    # MAKE LAST FAILED LOG OF USER SUCCESSFUL
    sub_log = SubscriptionLog.objects.filter(
        user__pk=user.pk, is_successful=False).order_by('-date', '-id').first()
    sub_log.is_successful = True
    # UPDATE USER SUBSCRIPTION DETAILS
    user_subscription = get_object_or_404(
        UserSubscription, profile__pk=user.pk)
    user_subscription.support_quest = quest_support == 1
    user_subscription.support_bookee = bookee_support == 1
    user_subscription.support_akada = akada_support == 1
    user_subscription.supported_grades = selected_grades.replace('%20', ' ')
    subscription_duration = duration
    user_subscription.expiry_date = date.today(
    ) + timedelta(days=int(subscription_duration))
    # SAVE CHANGES
    sub_log.save()
    user_subscription.save()
    return JsonResponse({
        'success': True,
        'message': 'Subscription successful!',
        'user_subscription': {
            'expiry_date': user_subscription.expiry_date,
            'support_quest': user_subscription.support_quest,
            'support_bookee': user_subscription.support_bookee,
            'support_akada': user_subscription.support_akada,
            'supported_grades': user_subscription.supported_grades.split(' --- '),
        },

    })
