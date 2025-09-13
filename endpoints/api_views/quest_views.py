import random
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from admin_app.models import *
from django.db.models import Avg, ExpressionWrapper, fields
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from admin_app.utils.grades import user_subscribed_grades
from akada.utils import NewStudyMaterialInstance, _save_study_materials_instance
from endpoints.api_views.subscription import is_subscription_valid


# ========================================================================================================
# QUESTS
# ========================================================================================================
def _build_quest_object(quest, username) -> dict[str, any]:
    if User.objects.filter(username=username).exists():
        answered_count = get_object_or_404(User, username=username).answered.filter(
            question__quest__pk=quest.pk).count()
    else:
        answered_count = 0
    avg_rating = quest.rated_quests.aggregate(avg_rating=ExpressionWrapper(
        Avg('rating'),
        output_field=fields.FloatField()
    ))['avg_rating']
    if avg_rating is not None:
        rating = f'{round(avg_rating, 1)}'
    else:
        rating = '5.0'

    return {
        'testid': quest.pk,
        'cover': quest.cover.url,
        'title': quest.title,
        'grade': quest.grade,
        'isPremium': quest.is_premium,
        'time': quest.time,
        'about': quest.about,
        'instructions': quest.instructions,
        'bookmarked': quest.bookmarked.filter(username=username).exists(),
        'question_count': quest.questions.count(),
        'answered_count': answered_count,
        'rating': rating,
        'topics': quest.questions.all().order_by('topic').values_list('topic', flat=True).distinct().count(),
    }


def _build_questions_list(questions) -> list[dict]:
    selected_questions = []

    for question in questions:
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
            'topic': question.topic,
            'is_draft': question.is_draft,
        })
    return selected_questions


def quests(request, username):
    search = request.GET.get('search')
    grade = request.GET.get('grade') or ''
    category = request.GET.get('category') or ''
    user = get_object_or_404(User, username=username)
    grades = user_subscribed_grades(user)
    quests = Quest.objects.filter(
        grade__icontains=grade, category__icontains=category, organization=None).order_by('?')
    if len(grades) > 0:
        quests = quests.filter(grade__in=grades)
    if search is not None:
        quests = quests.filter(
            title__icontains=search)
    paginator = Paginator(quests, 100)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        displayed_quests = paginator.page(page)
    except:
        displayed_quests = []
    quests_list = []
    for quest in displayed_quests:
        quests_list.append(_build_quest_object(quest, username))
    grade_list = Quest.objects.all().order_by(
        'grade').values_list('grade', flat=True).distinct()
    category_list = Quest.objects.all().order_by(
        'category').values_list('category', flat=True).distinct()
    list_of_grades = []
    list_of_categories = []
    for grade in grade_list:
        list_of_grades.append(grade)
    for category in category_list:
        list_of_categories.append(category)
    context = {
        'success': True,
        'quests': quests_list,
        'grades': list_of_grades,
        'categories': list_of_categories,
    }
    return JsonResponse(context)


def get_quest(request, testid, username):
    quest = get_object_or_404(Quest, id=testid)

    quest_obj = _build_quest_object(quest, username)
    context = {
        'success': True,
        'quest': quest_obj,
    }
    return JsonResponse(context)


def questions(request, testid, username):
    user = get_object_or_404(User, username=username)
    questions_order = request.GET.get('order') or None

    if not is_subscription_valid(user=user):
        return JsonResponse({
            'success': False,
            'message': 'Your subscription is expired!'
        })
    all_questions = Question.objects.filter(
        quest__pk=testid, is_draft=False).order_by('id')
    unanswered_questions = all_questions.exclude(
        answered_by__user__username=username).order_by('id')
    if questions_order == 'random':
        all_questions = all_questions.order_by('?')
        unanswered_questions = unanswered_questions.order_by('?')
    if unanswered_questions.count() > 0:
        random_items = list(unanswered_questions[:15])
    else:
        random_items = list(all_questions[:15])
    random.shuffle(random_items)

    context = {
        'success': True,
        'questions': _build_questions_list(random_items),
    }
    return JsonResponse(context)


def answer(request, questionids, username):
    for questionid in questionids.split(','):
        exists = AnsweredBy.objects.filter(
            user__username=username, question__id=int(questionid)).exists()
        if not exists:
            AnsweredBy.objects.create(
                user=get_object_or_404(User, username=username),
                question=get_object_or_404(Question, id=int(questionid))
            )
    else:
        return JsonResponse({'success': True})


def rate_quest(request, username, testid, rating):
    user = get_object_or_404(User, username=username)
    quest = get_object_or_404(Quest, id=testid)
    quest_rating = float(rating)
    if QuestRating.objects.filter(user__username=username, quest__id=testid).exists():
        for m_rating in QuestRating.objects.filter(user__username=username, quest__id=testid):
            m_rating.rating = quest_rating
            m_rating.save()
        return JsonResponse({'success': True, 'message': 'Rating has been updated'})
    else:
        instance = QuestRating()
        instance.user = user
        instance.quest = quest
        instance.rating = quest_rating
        instance.save()
        return JsonResponse({'success': True, 'message': 'Rating has been saved'})


def get_grades(request):
    grade_list = Quest.objects.all().order_by(
        'grade').values_list('grade', flat=True).distinct()
    list_of_grades = []
    for grade in grade_list:
        list_of_grades.append(grade)
    context = {
        'success': True,
        'grades': list_of_grades,
    }
    return JsonResponse(context)


# =================================================================================
# PRACTICE QUEST VIEWS
# =================================================================================
def get_quest_topics(request, testid) -> JsonResponse:
    """
    Returns an object list of all the topics in a quest along with the question count of each topic.
    """
    quest = get_object_or_404(Quest, id=testid)
    questions = Question.objects.filter(quest__pk=quest.pk)
    distinct_topics = questions.order_by('topic').values_list(
        'topic', flat=True).distinct()
    topics = []
    study_material_instances = []
    for topic in distinct_topics:
        topics.append({
            'testid': quest.id,
            'topic': topic,
            'question_count': questions.filter(topic=topic).count()
        })
        study_material_instances.append(NewStudyMaterialInstance(
            topic=topic,
            quest=quest
        ))
    _save_study_materials_instance(instances=study_material_instances)

    return JsonResponse({
        'success': True,
        'topics': topics,
    })


@require_POST
@csrf_exempt
def get_practice_questions(request, testid) -> JsonResponse:
    questions = Question.objects.filter(
        quest__pk=testid, topic=request.POST.get('topic'), is_draft=False).order_by('?')
    context = {
        'success': True,
        'questions': _build_questions_list(questions),
    }
    return JsonResponse(context)
