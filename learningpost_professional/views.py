import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from admin_app.models import Chapter, Library, Quest
from endpoints.api_views.quest_views import _build_quest_object
from learningpost_professional.models import ProfessionalOrganization, Test, TestAttempt, TestQuestion
from website.models import ProUserProfile, User
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
    year_of_birth = request.POST.get('year_of_birth')

    # VERIFY IF USER EXISTS
    user_exists = User.objects.filter(email=email).exists()
    if user_exists:
        return JsonResponse({
            'success': False,
            'message': 'User email has already been registered!',
        })

    # CREATE NEW USER
    user_instance = User()
    user_instance.first_name = first_name
    user_instance.last_name = last_name
    user_instance.email = email
    user_instance.username = username
    user_instance.set_password(password)
    user_instance.dob = datetime.datetime.strptime(
        f'01-01-{year_of_birth}', '%d-%M-%Y')
    user_instance.save()

    context = {
        'success': True,
        'message': 'Account Registered!',
    }
    return JsonResponse(context)


@require_POST
@csrf_exempt
def professional_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            auth.login(request, user=user)
            if not ProUserProfile.objects.filter(user__pk=user.pk).exists() or user.pro_profile.portrait is None:
                render_edit_profile = True
            else:
                render_edit_profile = False
            return JsonResponse({
                'success': True,
                'message': 'Login successful!',
                'render_edit_profile': render_edit_profile,
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                    'lastLogin': datetime.datetime.strftime(user.last_login, '%d-%m-%Y'),
                    'hasUnrestrictedAccess': user.is_superuser,
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
            'message': 'User not found!'
        })


@require_POST
@csrf_exempt
def update_pro_user_profile(request):
    portrait = request.FILES.get('portraitPhoto')
    user = get_object_or_404(User, email=request.POST.get('email'))
    if not ProUserProfile.objects.filter(user__pk=user.pk).exists():
        ProUserProfile.objects.create(user=user)
    user.pro_profile.portrait = portrait
    user.pro_profile.save()
    return JsonResponse({
        'success': True,
        'message': 'Profile updated!',
    })



@require_POST
@csrf_exempt
def add_learning_track(request):
    # GET POSTED DATA
    username = request.POST.get('username') or ''
    company_code = request.POST.get('cc') or ''

    # GET USER AND ORGANIZATION OBJECTS
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({
            'success': False,
            'message': 'Could not find a valid user.'
        })
    try:
        organization = ProfessionalOrganization.objects.get(
            organization_code=company_code)
    except:
        return JsonResponse({
            'success': False,
            'message': 'Group does not exist.'
        })
    # ADD USER TO ORGANIZATION
    organization.members.add(user)
    organization.save()

    return JsonResponse({
        'success': True,
        'message': f'Welcome to {organization.organization_name}',
    })


def get_learning_tracks(request, username):
    user = get_object_or_404(User, username=username)
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk)
    organizations_list = []
    for organization in organizations:
        organizations_list.append({
            'name': organization.organization_name,
            'logo': f'{organization.organization_logo.url}',
            'code': organization.organization_code,
        })
    context = {
        'success': True,
        'learning_tracks': organizations_list,
    }
    return JsonResponse(context)


def pro_quests(request, username):
    user = get_object_or_404(User, username=username)
    organization_code = request.GET.get('code') or None
    if organization_code is None or organization_code == '':
        return JsonResponse({
            'success': False,
            'message': 'Track not found!',
        })
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk, organization_code=organization_code)
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


def pro_library(request, username):
    user = get_object_or_404(User, username=username)
    organization_code = request.GET.get('code') or None
    if organization_code is None or organization_code == '':
        return JsonResponse({
            'success': False,
            'message': 'Track not found!',
        })
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk, organization_code=organization_code)
    books = Library.objects.filter(
        organization__in=organizations).order_by('?')
    search = request.GET.get('search')
    if search is not None:
        books = books.filter(title__icontains=search)
    books_list = []
    for book in books:
        books_list.append({
            'bookid': book.id,
            'cover': book.cover.url,
            'title': book.title,
            'about': book.about,
            'author': book.author,
            'about_author': book.about_author,
            'chapters_count': Chapter.objects.filter(book__id=book.id).count(),
        })
    context = {
        'success': True,
        'books': books_list
    }
    return JsonResponse(context)


def get_tests(request, username):
    user = get_object_or_404(User, username=username)
    organization_code = request.GET.get('code') or None
    if organization_code is None or organization_code == '':
        return JsonResponse({
            'success': False,
            'message': 'Track not found!',
        })
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk, organization_code=organization_code)
    tests = Test.objects.filter(organization__in=organizations)
    tests_list = [{
        'testid': test.pk,
        'title': test.title,
        'cover': test.cover.url,
        'time': test.time,
        'about': test.about,
        'instructions': test.instructions,
        'is_locked': test.expires <= datetime.date.today(),
        'is_attempted': test.attempts.all().filter(user__username=username).exists(),
        'status': 'Closed' if test.expires <= datetime.date.today() else f'Closes on {test.expires}',
        'question_count': test.test_questions.count(),
    } for test in tests]

    return JsonResponse({
        'success': True,
        'tests': tests_list,
    })


# TODO: CREATE A FUNCTION TO CREATE A TEST ATTEMPT INSTANCE.
# THE ATTEMPT SHOULD ONLY BE PERMITTED IF THE USER'S FACE SIMILARITY IS ABOVE 75%

def get_questions(request, testid):
    questions = TestQuestion.objects.filter(test__pk=testid).order_by('?')[:100]
    questions_list = []
    for question in questions:
        diagram_url = None
        if question.diagram:
            diagram_url = question.diagram.url
        questions_list.append({
            'testid': question.test.pk,
            'comprehension': question.comprehension,
            'diagram': diagram_url,
            'question': question.question,
            'a': question.a,
            'b': question.b,
            'c': question.c,
            'd': question.d,
            'answer': question.answer,
        })
    return JsonResponse({
        'success': True,
        'questions': questions_list,
    })


@require_POST
@csrf_exempt
def save_test_score(request, username: str, testid: int):
    try:
        score = request.POST.get('score')
        # user = User.objects.get(username=username)
        # test = Test.objects.get(pk=testid)
        attempts = TestAttempt.objects.filter(
            test__pk=testid, user__username=username)
        if attempts.exists():
            attempt = attempts.first()
            attempt.score = score
            attempt.save()
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid information provided',
            })
        return JsonResponse({
            'success': True,
            'message': 'Score has been saved!',
        })
    except:
        return JsonResponse({
            'success': False,
            'message': 'Invalid information provided',
        })


def get_score(request, username: str, testid: int):
    user = get_object_or_404(User, username=username)
    # organizations = ProfessionalOrganization.objects.filter(
    #     members__pk=user.pk)
    score = TestAttempt.objects.filter(
        test__pk=testid, user__username=username).first().to_json()
    if score is not None:
        return JsonResponse({
            'success': True,
            'score': score
        })
    else:
        return JsonResponse({
            'success': False,
            'message': "Couldn't find record of user's attempt"
        })
