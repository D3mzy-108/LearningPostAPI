from django.shortcuts import render, redirect, get_object_or_404
from .models import Quest, Question
import csv
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
def quests(request):
    search = request.GET.get('search_quest')
    search_val = ''
    if search is not None:
        search_val = search
        quests = Quest.objects.filter(title__icontains=search).order_by('-id')
    else:
        quests = Quest.objects.all().order_by('-id')
    paginator = Paginator(quests, 30)
    page = request.GET.get('page')
    if page == None:
        page = 1
    displayed_quests = paginator.page(page)

    context = {
        'quests': displayed_quests,
        'paginator': displayed_quests,
        'page': page,
        'search_val': search_val,
    }
    return render(request, 'admin_app/quests.html', context)


@login_required
def create_quest(request):
    if request.method == 'POST':
        title = request.POST['title']
        try:
            cover = request.FILES.get('cover')
        except:
            return redirect('create_quest')
        grade = request.POST['grade']
        time = request.POST['time']
        about = request.POST['about']
        instructions = request.POST['instructions']
        quest_type = request.POST['quest_type']

        instance = Quest()
        instance.title = title
        instance.cover = cover
        instance.grade = grade
        instance.time = time
        instance.about = about
        instance.instructions = instructions
        instance.quest_type = quest_type
        instance.save()
        return redirect('quests')
    context = {}
    return render(request, 'admin_app/quest_form.html', context)


@login_required
def edit_quest(request, pk):
    instance = get_object_or_404(Quest, pk=pk)
    if request.method == 'POST':
        instance.title = request.POST['title']
        cover = request.FILES.get('cover')
        if cover is not None:
            instance.cover = cover
        instance.grade = request.POST['grade']
        instance.time = request.POST['time']
        instance.about = request.POST['about']
        instance.instructions = request.POST['instructions']
        instance.quest_type = request.POST['quest_type']
        instance.save()
        return redirect('quests')
    context = {
        'instance': instance
    }
    return render(request, 'admin_app/quest_form.html', context)


@login_required
def delete_quest(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    quest.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def view_questions(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    search = request.GET.get('search_questions')
    search_val = ''
    if search is not None:
        questions = quest.questions.all().filter(
            question__icontains=search).order_by('-id')
        search_val = search
    else:
        questions = quest.questions.all().order_by('-id')
    paginator = Paginator(questions, 30)
    page = request.GET.get('page')
    if page == None:
        page = 1
    displayed_questsions = paginator.page(page)
    context = {
        'quest': quest,
        'questions': displayed_questsions,
        'paginator': displayed_questsions,
        'page': page,
        'search_val': search_val,
    }
    return render(request, 'admin_app/quest_questions.html', context)


@login_required
def bulk_upload(request, pk):
    if request.method == 'POST':
        questions_file = request.FILES.get('questions')
        decoded_file = questions_file.read().decode('utf-8').splitlines()
        delimiter = ',' if questions_file.name.endswith('.csv') else '\t'
        reader = csv.DictReader(decoded_file, delimiter=delimiter)
        table_heads = next(csv.reader(decoded_file, delimiter=delimiter), None)
        rows = list(reader)
        for row in rows:
            question = Question()
            question.quest = get_object_or_404(Quest, pk=pk)
            question.comprehension = row[table_heads[0]]
            question.question = row[table_heads[1]]
            question.a = row[table_heads[2]]
            question.b = row[table_heads[3]]
            question.c = row[table_heads[4]]
            question.d = row[table_heads[5]]
            question.answer = row[table_heads[6]]
            question.explanation = row[table_heads[7]]
            question.save()
    return redirect('view_questions', pk=pk)


@login_required
def single_upload(request, pk):
    if request.method == 'POST':
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
        question.save()
    return redirect('view_questions', pk=pk)


@login_required
def edit_question(request, quest_pk, pk):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=pk)
        diagram = request.FILES.get('diagram')
        if diagram is not None:
            question.diagram = diagram
        if request.POST.get('clear_diagram') is not None and request.POST.get('clear_diagram') == 'on':
            question.diagram = None
        question.comprehension = f"{request.POST['comprehension']}"
        question.question = request.POST['question']
        question.a = request.POST['a']
        question.b = request.POST['b']
        question.c = request.POST['c']
        question.d = request.POST['d']
        question.answer = request.POST['answer']
        question.explanation = request.POST['explanation']
        question.save()
    return redirect('view_questions', pk=quest_pk)


@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect(request.META.get('HTTP_REFERER'))
