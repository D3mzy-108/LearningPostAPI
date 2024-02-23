from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from website.models import SubAccounts, User, UserProfile, BetaReferal
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt


# ========================================================================================================
# AUTH
# ========================================================================================================
@csrf_exempt
def login_endpoint(request):
    if request.method == 'POST':
        # Extract user data from the request
        user_id = request.POST.get('userId')
        display_name = request.POST.get('displayName')
        email = request.POST.get('email')
        profileUrl = request.POST.get('profileURL')
        # Add other necessary user information

        # Check if the user already exists
        user, created = User.objects.get_or_create(
            username=user_id, defaults={'email': email})

        # If the user is newly created, set additional attributes
        if created:
            user.first_name = display_name
            user.profile_photo = profileUrl
            # Set other user attributes as needed
            user.save()

        # Login the user
        auth.login(request, user)

        profile = UserProfile.objects.filter(user__pk=user.pk)
        if profile.exists():
            rc = ''
            if BetaReferal.objects.filter(profile__pk=profile.first().pk):
                rc = profile.first().referral.code
            user_profile = {
                'phone': profile.first().phone,
                'date_of_birth': profile.first().date_of_birth,
                'school': profile.first().school,
                'referal_code': rc,
                'country': profile.first().country,
                'state': profile.first().state,
                'guardian_email': profile.first().guardian_email,
                'guardian_phone': profile.first().guardian_phone,
            }
        else:
            user_profile = {
                'phone': '',
                'date_of_birth': '',
                'school': '',
                'referal_code': '',
                'country': '',
                'state': '',
                'guardian_email': '',
                'guardian_phone': '',
            }
        context = {
            'success': True,
            'message': 'Login Successful!',
            'isNewUser': not profile.exists(),
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
    profiles = UserProfile.objects.filter(user__pk=user.pk)
    if not profiles.exists():
        profile = UserProfile()
        profile.user = user
    else:
        profile = profiles.first()
    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.date_of_birth = request.POST.get('dob')
        profile.school = request.POST.get('school')
        profile.country = request.POST.get('country')
        profile.state = request.POST.get('state')
        profile.guardian_email = request.POST.get('guardian_email')
        profile.guardian_phone = request.POST.get('guardian_phone')
        referal_code = request.POST.get('ref_code')
        referral = BetaReferal.objects.filter(code=referal_code)
        if referral.exists():
            m_ref = referral.first()
            if not m_ref.is_used:
                profile.save()
                m_ref.is_used = True
                m_ref.profile = profile
                m_ref.save()
                message = 'Your profile has been updated!'
            else:
                if m_ref.profile.user.pk == profile.user.pk:
                    profile.save()
                    message = 'Your profile has been updated!'
                else:
                    message = 'Referral has already been used!'
            return JsonResponse({
                'success': True,
                'message': message,
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid referral code!',
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request!',
    })


def get_logged_in_user(request, username):
    user = User.objects.filter(username=username)
    user_profile = {
        'phone': '',
        'date_of_birth': '',
        'school': '',
        'referal_code': '',
        'country': '',
        'state': '',
        'guardian_email': '',
        'guardian_phone': '',
    }
    if user.exists():
        m_user = get_object_or_404(User, username=username)
        userid = m_user.username
        display_name = m_user.first_name
        email = m_user.email
        profile_url = m_user.profile_photo
        profile = UserProfile.objects.filter(user__pk=m_user.pk)
        rc = ''
        if BetaReferal.objects.filter(profile__pk=profile.first().pk):
            rc = profile.first().referral.code
        if profile.exists():
            user_profile = {
                'phone': profile.first().phone,
                'date_of_birth': profile.first().date_of_birth,
                'school': profile.first().school,
                'referal_code': rc,
                'country': profile.first().country,
                'state': profile.first().state,
                'guardian_email': profile.first().guardian_email,
                'guardian_phone': profile.first().guardian_phone,
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
        code = request.POST.get('ref_code')
        referral = get_object_or_404(BetaReferal, code=code)
        if referral.profile is not None:
            child = referral.profile.user
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
