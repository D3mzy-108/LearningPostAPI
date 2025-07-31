import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from admin_app.utils.csv_file_upload_manager import parse_questions_from_csv
from learningpost_professional.models import ProfessionalOrganization, Test, TestQuestion
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator


def _build_test_object(test):
    return {
        'id': test.pk,
        'cover': test.cover.url,
        'title': test.title,
        'time': test.time,
        'about': test.about or '',
        'instructions': test.instructions or '',
        'organization': test.organization.organization_code,
        'attempts': test.participants.all().count(),
        'status': 'Closed' if test.expires <= datetime.date.today() else f'Closes on {test.expires}',
        'expires': f'{test.expires}',
    }

def _build_test_questions_list(questions):
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
            'explanation': '',
            'topic': '',
        })
    return selected_questions


def get_partners(request):
    partners = ProfessionalOrganization.objects.all().order_by('-id')
    return JsonResponse({
        'success': True,
        'partners': [
            {
                'id': partner.pk,
                'name': partner.organization_name,
                'logo': partner.organization_logo.url,
                'code': partner.organization_code,
            } for partner in partners
        ],
    })


def get_partner_tests(request):
    organization_code = request.GET.get('code') or None
    search = request.GET.get('q') or ''
    tests = Test.objects.filter(title__icontains=search, organization__organization_code=organization_code)
    return JsonResponse({
        'success': True,
        'tests': [
            _build_test_object(test) for test in tests
        ],
    })


@require_POST
@csrf_exempt
def save_test_instance(request):
    test_id = request.POST.get('id')
    cover = request.FILES.get('cover')
    title = request.POST.get('title')
    time = request.POST.get('time')
    about = request.POST.get('about')
    instructions = request.POST.get('instructions')
    organization_code = request.POST.get('organization_code')
    expires = request.POST.get('expires')
    
    if test_id == None or test_id == '':
        test = Test()
    else:
        test = get_object_or_404(Test, pk=test_id)
    if cover is not None:
        test.cover = cover
    test.title = title
    test.time = time
    test.about = about
    test.instructions = instructions
    test.expires = expires
    test.organization = get_object_or_404(ProfessionalOrganization, organization_code=organization_code)
    test.save()
    return JsonResponse({'success': True, 'message': 'Test instance saved!'})
            

def view_test_questions(request, pk):
    test = get_object_or_404(Test, pk=pk)
    search = request.GET.get('search_questions')
    questions = test.test_questions.all().order_by('-id')
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
        'test': _build_test_object(test),
        'questions': _build_test_questions_list(displayed_questions),
        'page': f'{page} of {displayed_questions.paginator.num_pages}',
        'num_pages': displayed_questions.paginator.num_pages,
        'search_val': search_val,
        'question_count': questions.count(),
    }
    return JsonResponse(context)


@require_POST
@csrf_exempt
def bulk_upload_test_question(request, pk):
    questions_file = request.FILES.get('questions')
    table_heads, rows = parse_questions_from_csv(questions_file)
    if table_heads is None and len(table_heads) > 6:
        return JsonResponse({'success': False, 'message': 'Invalid file format'})
    for row in rows:
        answer_options = [row[table_heads[2]], row[table_heads[3]], row[table_heads[4]], row[table_heads[5]]]
        question = TestQuestion()
        question.test = get_object_or_404(Test, pk=pk)
        question.comprehension = row[table_heads[0]]
        question.question = row[table_heads[1]]
        question.a = row[table_heads[2]]
        question.b = row[table_heads[3]]
        question.c = row[table_heads[4]]
        question.d = row[table_heads[5]]
        
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
def single_upload_test_question(request, pk):
    if request.POST.get('questionId') is not None and not request.POST.get('questionId') == '':
        question = get_object_or_404(TestQuestion, id=request.POST.get('questionId'))
    else:
        question = TestQuestion()

    question.test = get_object_or_404(Test, pk=pk)
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
    question.save()
    return JsonResponse({'success': True, 'message': 'Saved question instance!'})

