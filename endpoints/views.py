from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from admin_app.models import Quest, Question, AnsweredBy
from website.models import User, UserProfile, BetaReferal
# from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt


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
    else:
        userid = None
        display_name = 'Guest User'
        email = None
        profile_url = ''
    context = {
        'userId': userid,
        'displayName': display_name,
        'email': email,
        'profileURL': profile_url,
        'userProfile': user_profile,
    }
    return JsonResponse(context)


def quests(request, username):
    quests = Quest.objects.all().order_by('-id')
    search = request.GET.get('search')
    if search is not None:
        quests = quests.filter(title__icontains=search)
    paginator = Paginator(quests, 10)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        displayed_quests = paginator.page(page)
    except:
        displayed_quests = []
    quests_list = []
    for quest in displayed_quests:
        if User.objects.filter(username=username).exists():
            answered_count = get_object_or_404(User, username=username).answered.filter(
                question__quest__pk=quest.pk).count()
        else:
            answered_count = 0
        quests_list.append({
            'testid': quest.pk,
            'cover': quest.cover.url,
            'title': quest.title,
            'grade': quest.grade,
            'time': quest.time,
            'about': quest.about,
            'instructions': quest.instructions,
            'bookmarked': quest.bookmarked.filter(username=username).exists(),
            'question_count': quest.questions.count(),
            'answered_count': answered_count,
        })
    context = {
        'success': True,
        'quests': quests_list,
    }
    return JsonResponse(context)


def questions(request, testid, username):
    all_questions = Question.objects.filter(quest__pk=testid).order_by('?')
    unanswered_questions = all_questions.exclude(
        answered_by__user__username=username).order_by('?')
    if unanswered_questions.count() > 0:
        random_items = unanswered_questions[:30]
    else:
        random_items = all_questions[:30]
    selected_questions = []

    for question in random_items:
        diagram_url = None
        if question.diagram:
            diagram_url = question.diagram.url
        selected_questions.append({
            'questionid': question.pk,
            'comprehension': question.comprehension,
            'diagram': diagram_url,
            'question': question.question,
            'a': question.a,
            'b': question.b,
            'c': question.c,
            'd': question.d,
            'answer': question.answer,
            'explanation': question.explanation,
        })
    context = {
        'success': True,
        'questions': selected_questions,
    }
    return JsonResponse(context)


def answer(request, questionid, username):
    exists = AnsweredBy.objects.filter(
        user__username=username, question__id=questionid).exists()
    if not exists:
        AnsweredBy.objects.create(
            user=get_object_or_404(User, username=username),
            question=get_object_or_404(Question, id=questionid)
        )
    return JsonResponse({'success': True})


def bookmarks(request, username):
    if User.objects.filter(username=username).exists():
        bookmarked_quests = Quest.objects.filter(
            bookmarked__username=username).order_by('title')
    else:
        bookmarked_quests = []
    paginator = Paginator(bookmarked_quests, 10)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        displayed_quests = paginator.page(page)
    except:
        displayed_quests = []
    bookmark_list = []
    for quest in displayed_quests:
        if User.objects.filter(username=username).exists():
            answered_count = get_object_or_404(User, username=username).answered.filter(
                question__quest__pk=quest.pk).count()
        else:
            answered_count = 0
        bookmark_list.append({
            'testid': quest.pk,
            'cover': quest.cover.url,
            'title': quest.title,
            'grade': quest.grade,
            'time': quest.time,
            'instructions': quest.instructions,
            'bookmarked': quest.bookmarked.filter(username=username).exists(),
            'question_count': quest.questions.count(),
            'answered_count': answered_count,
        })
    else:
        context = {
            'success': True,
            'quests': bookmark_list,
        }
        return JsonResponse(context)


def add_to_bookmark(request, username, testid, is_adding):
    quest = get_object_or_404(Quest, pk=testid)
    user = get_object_or_404(User, username=username)
    if is_adding == 'true':
        quest.bookmarked.add(user)
        message = f'Saved {quest.title} to your bookmarks'
    else:
        quest.bookmarked.remove(user)
        message = f'Removed {quest.title} from your bookmarks'
    quest.save()
    context = {
        'success': True,
        'message': message,
    }
    return JsonResponse(context)
