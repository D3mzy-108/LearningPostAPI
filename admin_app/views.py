import string
import random
from django.shortcuts import render, redirect, get_object_or_404
from website.models import BetaReferal
from .models import *
import csv
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# ========================================================================================================
# QUESTS
# ========================================================================================================

@login_required
def quests(request):
    search = request.GET.get('search_quest')
    search_val = ''
    if search is not None:
        search_val = search
        quests = Quest.objects.filter(title__icontains=search).order_by('?')
    else:
        quests = Quest.objects.all().order_by('?')
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
    return render(request, 'admin_app/quests/quests.html', context)


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
    return render(request, 'admin_app/quests/quest_form.html', context)


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
    return render(request, 'admin_app/quests/quest_form.html', context)


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
    return render(request, 'admin_app/quests/quest_questions.html', context)


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


# ========================================================================================================
# CLASSIFICATIONS
# ========================================================================================================

@login_required
def classifications(request):
    referrals = BetaReferal.objects.all().order_by('-id')
    context = {
        'referrals': referrals,
    }
    return render(request, 'admin_app/classifications/classifications.html', context)


@login_required
def generate_new_code(request):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(15))
    if not BetaReferal.objects.filter(code=random_string).exists():
        referal = BetaReferal()
        referal.code = random_string
        referal.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_code(request, id):
    referral = get_object_or_404(BetaReferal, id=id)
    profile = referral.profile
    if profile is not None:
        profile.delete()
    referral.delete()
    return redirect(request.META.get('HTTP_REFERER'))


# ========================================================================================================
# LIBRARY
# ========================================================================================================

@login_required
def library(request):
    search = request.GET.get('search_books')
    search_val = ''
    if search is not None:
        search_val = search
        books = Library.objects.filter(title__icontains=search).order_by('?')
    else:
        books = Library.objects.all().order_by('?')
    paginator = Paginator(books, 30)
    page = request.GET.get('page')
    if page == None:
        page = 1
    displayed_books = paginator.page(page)

    context = {
        'library': displayed_books,
        'paginator': displayed_books,
        'page': page,
        'search_val': search_val,
    }
    return render(request, 'admin_app/library/library.html', context)


@login_required
def create_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        try:
            cover = request.FILES.get('cover')
        except:
            return redirect('create_quest')
        about = request.POST['about']

        instance = Library()
        instance.title = title
        instance.cover = cover
        instance.about = about
        instance.save()
        return redirect('library')
    context = {}
    return render(request, 'admin_app/library/book_form.html', context)


@login_required
def edit_book(request, pk):
    instance = get_object_or_404(Library, pk=pk)
    if request.method == 'POST':
        instance.title = request.POST['title']
        cover = request.FILES.get('cover')
        if cover is not None:
            instance.cover = cover
        instance.about = request.POST['about']
        instance.save()
        return redirect('library')
    context = {
        'instance': instance
    }
    return render(request, 'admin_app/library/book_form.html', context)


@login_required
def delete_book(request, pk):
    get_object_or_404(Library, pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def view_book(request, pk):
    book = get_object_or_404(Library, pk=pk)
    context = {
        'book': book,
        'chapters': book.chapters.all(),
    }
    return render(request, 'admin_app/library/book_details.html', context)


@login_required
def upload_chapter(request, pk):
    chapter = Chapter()
    chapter.title = request.POST.get('title')
    chapter.chapter_file = request.FILES.get('chapter')
    chapter.book = get_object_or_404(Library, pk=pk)
    chapter.save()
    return redirect('view_book', pk=pk)


@login_required
def delete_chapter(request, pk):
    get_object_or_404(Chapter, pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))
