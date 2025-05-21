from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from admin_app.models import *
from admin_app.utils.grades import user_subscribed_grades
from website.models import User
from django.db.models import Avg, ExpressionWrapper, fields


# ========================================================================================================
# BOOKMARKS
# ========================================================================================================
def bookmarks(request, username):
    if User.objects.filter(username=username).exists():
        bookmarked_quests = Quest.objects.filter(
            bookmarked__username=username).order_by('title')
        bookmarked_books = Library.objects.filter(
            bookmarked__username=username).order_by('title')

        user = get_object_or_404(User, username=username)
        grades = user_subscribed_grades(user)
        if len(grades) > 0:
            bookmarked_quests = bookmarked_quests.filter(grade__in=grades)
    else:
        bookmarked_quests = []
        bookmarked_books = []

    # BOOKMARKED QUESTS
    quests_paginator = Paginator(bookmarked_quests, 50)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        displayed_quests = quests_paginator.page(page)
    except:
        displayed_quests = []
    quest_list = []
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
        quest_list.append({
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
        })

    # BOOKMARKED BOOKS
    books_paginator = Paginator(bookmarked_books, 50)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        displayed_books = books_paginator.page(page)
    except:
        displayed_books = []
    book_list = []
    for book in displayed_books:
        avg_rating = book.rated_books.aggregate(avg_rating=ExpressionWrapper(
            Avg('rating'),
            output_field=fields.FloatField()
        ))['avg_rating']
        if avg_rating is not None:
            rating = f'{round(avg_rating, 1)}'
        else:
            rating = '5.0'
        book_list.append({
            'bookid': book.pk,
            'cover': book.cover.url,
            'title': book.title,
            'about': book.about,
            'author': book.author,
            'about_author': book.about_author,
            'isPremium': book.is_premium,
            'bookmarked': book.bookmarked.filter(username=username).exists(),
            'chapters_count': book.chapters.count(),
            'rating': rating,
        })

    # RETURNED CONTEXT
    context = {
        'success': True,
        'quests': quest_list,
        'books': book_list,
    }
    return JsonResponse(context)


def add_quest_to_bookmark(request, username, testid, is_adding):
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


def add_book_to_bookmark(request, username, bookid, is_adding):
    book = get_object_or_404(Library, pk=bookid)
    user = get_object_or_404(User, username=username)
    if is_adding == 'true':
        book.bookmarked.add(user)
        message = f'Saved {book.title} to your bookmarks'
    else:
        book.bookmarked.remove(user)
        message = f'Removed {book.title} from your bookmarks'
    book.save()
    context = {
        'success': True,
        'message': message,
    }
    return JsonResponse(context)
