from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from admin_app.models import Quest
from endpoints.api_views.quest_views import _build_quest_object
from learningpost_professional.models import ProfessionalOrganization
from website.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import auth


@require_POST
@csrf_exempt
def professional_signup(request):
    first_name = request.POST.get('first_name') or ''
    last_name = request.POST.get('last_name') or ''
    email = request.POST.get('email')
    username = request.POST.get('username') or email.split('@')[0]
    password = request.POST.get('password')
    company_code = request.POST.get('company_code')

    if not User.objects.filter(username=username).exists():
        user_instance = User()
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.email = email
        user_instance.username = username
        user_instance.set_password(password)
        user_instance.save()

    user = get_object_or_404(User, username=username)
    organization = get_object_or_404(
        ProfessionalOrganization, organization_code=company_code)
    organization.members.add(user)
    organization.save()

    return JsonResponse({
        'success': True,
        'message': 'Account Registered!',
    })


@require_POST
@csrf_exempt
def professional_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            auth.login(request, user=user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful!',
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                },
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials!'
            })
    except:
        return JsonResponse({
            'success': False,
            'message': 'Invalid credentials!'
        })


def pro_quests(request, username):
    user = get_object_or_404(User, username=username)
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk)
    quests = Quest.objects.filter(organization__in=organizations).order_by('?')

    search = request.GET.get('search')
    if search is not None:
        quests = quests.filter(
            title__icontains=search)
    quests_list = []
    for quest in quests:
        quests_list.append(_build_quest_object(quest, username))
    context = {
        'success': True,
        'quests': quests_list,
    }
    return JsonResponse(context)
