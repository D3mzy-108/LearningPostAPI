import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from admin_app.models import Chapter, Library, Quest
from endpoints.api_views.quest_views import _build_quest_object
from learningpost_professional.models import ProfessionalOrganization, Score, Test, TestQuestion
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

    # VERIFY ORGANIZATION CODE
    organization = get_object_or_404(
        ProfessionalOrganization, organization_code=company_code)

    # VERIFY IF USER EXISTS
    user_exists = User.objects.filter(email=email).exists()
    if user_exists:
        return JsonResponse({
            'success': False,
            'message': 'User email has already been registered!',
        })

    # CREATE NEW USER
    if not User.objects.filter(username=username).exists():
        user_instance = User()
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.email = email
        user_instance.username = username
        user_instance.set_password(password)
        user_instance.save()

    # ADD USER TO ORGANIZATION
    user = get_object_or_404(User, username=username)
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


def pro_library(request, username):
    user = get_object_or_404(User, username=username)
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk)
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
    organizations = ProfessionalOrganization.objects.filter(
        members__pk=user.pk)
    tests = Test.objects.filter(organization__in=organizations)
    tests_list = [{
        'testid': test.pk,
        'title': test.title,
        'cover': test.cover.url,
        'time': test.time,
        'about': test.about,
        'instructions': test.instructions,
        'is_locked': test.expires <= datetime.date.today(),
        'is_attempted': test.participants.all().filter(user__username=username).exists(),
        'status': 'Closed' if test.expires <= datetime.date.today() else f'Closes on {test.expires}',
        'question_count': test.test_questions.count(),
    } for test in tests]

    return JsonResponse({
        'success': True,
        'tests': tests_list,
    })


def get_questions(request, testid):
    questions = TestQuestion.objects.filter(test__pk=testid)
    questions_list = []
    for question in questions
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
        'tests': questions_list,
    })


@require_POST
@csrf_exempt
def save_test_score(request, username: str, testid: int):
    try:
        score = request.POST.get('score')
        user = User.objects.get(username=username)
        test = Test.objects.get(pk=testid)
        score_instance = Score()
        score_instance.user = user
        score_instance.test = test
        score_instance.score = score
        score_instance.save()
        return JsonResponse({
            'success': True,
            'message': 'Score has been saved!',
        })
    except:
        return JsonResponse({
            'success': False,
            'message': 'Invalid information provided',
        })
