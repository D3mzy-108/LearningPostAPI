from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from admin_app.utils.csv_file_upload_manager import parse_questions_from_csv
from admin_app.utils.grades import get_grades_list
from endpoints.api_views.quest_views import _build_questions_list
from ..models import *
import csv
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


# ========================================================================================================
# QUESTS
# ========================================================================================================

def _build_quest_object(quest):
    return {
        'id': quest.pk,
        'cover': quest.cover.url,
        'title': quest.title,
        'grade': quest.grade,
        'category': quest.category or '',
        'time': quest.time,
        'bookmark_count': quest.bookmarked.count(),
        'question_count': quest.questions.count(),
        'rating': quest.average_rating(),
        'about': quest.about,
        'instructions': quest.instructions,
        'organization': quest.organization.organization_code if quest.organization else None,
    }

def quests(request):
    search = request.GET.get('search_quest') or None
    code = request.GET.get('code') or None
    if code is not None and code != '':
        quests = Quest.objects.filter(organization__organization_code=code).order_by('-id')
    else:
        quests = Quest.objects.filter(organization=None).order_by('-id')
    if search is not None:
        quests = quests.filter(title__icontains=search).order_by('-id')
    paginator = Paginator(quests, 50)
    page = request.GET.get('page')
    if page == None or int(page) > paginator.num_pages or int(page) < 1:
        page = 1
    displayed_quests = paginator.page(page)

    context = {
        'success': True,
        'quests': [
            _build_quest_object(quest) for quest in displayed_quests
        ],
        'page': f'{page} of {displayed_quests.paginator.num_pages}',
        'num_pages': displayed_quests.paginator.num_pages,
        'search_val': search or '',
    }
    return JsonResponse(context)

@require_POST
@csrf_exempt
def submit_quest(request):
    quest_id = request.POST.get('id')
    title = request.POST['title']
    cover = request.FILES.get('cover')
    grade = request.POST['grade']
    category = request.POST['category']
    time = request.POST['time']
    about = request.POST['about']
    instructions = request.POST['instructions']
    organization_code = request.POST.get('organization_code')

    if organization_code is not None and organization_code != '':
        organization = get_object_or_404(
            ProfessionalOrganization, organization_code=organization_code)
    else:
        organization = None

    if quest_id == None or quest_id == '':

        Quest.objects.create(
            title=title,
            cover=cover,
            grade=grade,
            category=category,
            time=time,
            about=about,
            instructions=instructions,
            organization=organization,
        )
    else:
        instance = get_object_or_404(Quest, pk=quest_id)
        instance.title = request.POST['title']
        cover = request.FILES.get('cover')
        if cover is not None:
            instance.cover = cover
        instance.grade = request.POST['grade']
        instance.category = request.POST['category']
        instance.time = request.POST['time']
        instance.about = request.POST['about']
        instance.instructions = request.POST['instructions']
        instance.organization = organization
        instance.save()
    return JsonResponse({'success': True, 'message': 'Quest saved successfully'})


def view_questions(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    search = request.GET.get('search_questions')
    questions = quest.questions.all().order_by('-id')
    search_val = ''
    if search is not None:
        questions = questions.filter(question__icontains=search)
        search_val = search

    paginator = Paginator(questions, 30)
    page = request.GET.get('page')
    if page == None:
        page = 1

    displayed_questions = paginator.page(page)
    context = {
        'success': True,
        'quest': _build_quest_object(quest),
        'questions': _build_questions_list(displayed_questions),
        'page': f'{page} of {displayed_questions.paginator.num_pages}',
        'num_pages': displayed_questions.paginator.num_pages,
        'search_val': search_val,
    }
    return JsonResponse(context)


@require_POST
@csrf_exempt
def bulk_upload(request, pk):
    questions_file = request.FILES.get('questions')
    table_heads, rows = parse_questions_from_csv(questions_file)
    if table_heads is None and len(table_heads) != 9:
        return JsonResponse({'success': False, 'message': 'Invalid file format'})
    for row in rows:
        answer_options = [row[table_heads[2]], row[table_heads[3]], row[table_heads[4]], row[table_heads[5]]]
        question = Question()
        question.quest = get_object_or_404(Quest, pk=pk)
        question.comprehension = row[table_heads[0]]
        question.question = row[table_heads[1]]
        question.a = row[table_heads[2]]
        question.b = row[table_heads[3]]
        question.c = row[table_heads[4]]
        question.d = row[table_heads[5]]
        question.explanation = row[table_heads[7]]
        question.topic = row[table_heads[8]]
        
        if row[table_heads[6]] in answer_options:
            question.answer = row[table_heads[6]]
            question.save()
        else:
            if row[table_heads[6]].lower() in ['a', 'b', 'c', 'd']:
                question.answer = answer_options[['a', 'b', 'c', 'd'].index(row[table_heads[6]].lower())]
                question.save()
            else:
                pass

    return JsonResponse({'success': True, 'message': 'Questions saved successfully'})


@require_POST
@csrf_exempt
def single_upload(request, pk):
    if request.POST.get('questionId') is not None and not request.POST.get('questionId') == '':
        question = get_object_or_404(Question, id=request.POST.get('questionId'))
    else:
        question = Question()

    question.quest = get_object_or_404(Quest, pk=pk)
    diagram = request.FILES.get('diagram')
    if diagram is not None:
        question.diagram = diagram
    question.comprehension = f"{request.POST['comprehension']}"
    question.question = request.POST['question']
    question.a = request.POST['a']
    question.b = request.POST['b']
    question.c = request.POST['c']
    question.d = request.POST['d']
    question.answer = request.POST['answer']
    question.explanation = request.POST['explanation']
    question.topic = request.POST['topic']
    question.save()
    return JsonResponse({'success': True, 'message': 'Saved question instance!'})


def download_quest(request, testid):
    quest = get_object_or_404(Quest, id=testid)
    questions = Question.objects.filter(quest__id=quest.pk)
    # Set the response content type to TSV
    response = HttpResponse(content_type='text/tab-separated-values')
    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = f'attachment; filename="{quest.title}.tsv"'
    # Write the header
    if questions.count() > 0:
        # Create a TSV writer
        tsv_writer = csv.writer(response, delimiter='\t')
        header = ['comprehension', 'diagram', 'question',
                  'a', 'b', 'c', 'd', 'answer', 'explanation', 'topic']
        tsv_writer.writerow(header)
        # Write the data
        for item in questions.values():
            tsv_writer.writerow([
                item['comprehension'],
                item['diagram'],
                item['question'],
                item['a'],
                item['b'],
                item['c'],
                item['d'],
                item['answer'],
                item['explanation'],
                item['topic'],
            ])

    return response
