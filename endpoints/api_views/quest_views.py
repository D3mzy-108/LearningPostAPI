from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from admin_app.models import *
from django.db.models import Avg, ExpressionWrapper, fields


# ========================================================================================================
# QUESTS
# ========================================================================================================
def quests(request, username):
    quests = Quest.objects.all().order_by('?')
    search = request.GET.get('search')
    if search is not None:
        quests = quests.filter(title__icontains=search)
    paginator = Paginator(quests, 50)
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
        avg_rating = quest.rated_quests.aggregate(avg_rating=ExpressionWrapper(
            Avg('rating'),
            output_field=fields.FloatField()
        ))['avg_rating']
        if avg_rating is not None:
            rating = f'{round(avg_rating, 1)}'
        else:
            rating = '5.0'

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
            'rating': rating,
        })
    context = {
        'success': True,
        'quests': quests_list,
    }
    return JsonResponse(context)


def get_quest(request, testid, username):
    quest = get_object_or_404(Quest, id=testid)
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

    quest_obj = {
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
        'rating': rating,
    }
    context = {
        'success': True,
        'quest': quest_obj,
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


def download_questions(request, testid, username):
    all_questions = Question.objects.filter(quest__pk=testid).order_by('?')
    random_items = all_questions[:300]
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
