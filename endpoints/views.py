from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from admin_app.models import Quest, Question, AnsweredBy
from website.models import User


def login(request):
    context = {}
    return JsonResponse(context)


def quests(request):
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
        quests_list.append({
            'testid': quest.pk,
            'cover': quest.cover.url,
            'title': quest.title,
            'grade': quest.grade,
            'time': quest.time,
            'instructions': quest.instructions,
            'bookmarked': quest.bookmarked.filter(pk=request.user.pk).exists(),
            'question_count': quest.questions.count(),
            'answered_count': request.user.answered.filter(question__quest__pk=quest.pk),
        })
    context = {
        'success': True,
        'quests': quests_list,
    }
    return JsonResponse(context)


def questions(request, testid):
    all_questions = Question.objects.filter(quest__pk=testid).order_by('?')
    unanswered_questions = all_questions.exclude(
        answered_by__user__pk=request.user.pk)
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


def answer(request, questionid):
    AnsweredBy.objects.create(
        user=get_object_or_404(User, pk=request.user.id),
        question=get_object_or_404(Question, id=questionid)
    )
    return JsonResponse({'success': True})
