from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from admin_app.models import *
from django.db.models import Avg, ExpressionWrapper, fields


# ========================================================================================================
# LIBRARY
# ========================================================================================================
def library(request, username):
    books = Library.objects.all().order_by('?')
    search = request.GET.get('search')
    if search is not None:
        books = books.filter(title__icontains=search)
    paginator = Paginator(books, 50)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        displayed_books = paginator.page(page)
    except:
        displayed_books = []
    books_list = []
    for book in displayed_books:
        avg_rating = book.rated_books.aggregate(avg_rating=ExpressionWrapper(
            Avg('rating'),
            output_field=fields.FloatField()
        ))['avg_rating']
        if avg_rating is not None:
            rating = f'{round(avg_rating, 1)}'
        else:
            rating = '5.0'

        books_list.append({
            'bookid': book.id,
            'cover': book.cover.url,
            'title': book.title,
            'about': book.about,
            'about_author': book.about_author,
            'bookmarked': book.bookmarked.filter(username=username).exists(),
            'chapters_count': Chapter.objects.filter(book__id=book.id).count(),
            'rating': rating,
        })
    context = {
        'success': True,
        'books': books_list
    }
    return JsonResponse(context)


def chapters(request, username, bookid):
    chapters = Chapter.objects.filter(book__id=bookid).order_by('title')
    list_of_chapters = []
    for chapter in chapters:
        list_of_chapters.append({
            'title': chapter.title,
            'file': chapter.chapter_file.url,
        })
    context = {
        'success': True,
        'chapters': list_of_chapters,
    }
    return JsonResponse(context)


def rate_book(request, username, bookid, rating):
    user = get_object_or_404(User, username=username)
    book = get_object_or_404(Library, id=bookid)
    book_rating = float(rating)
    if LibraryRating.objects.filter(user__username=username, book__id=bookid).exists():
        for m_rating in LibraryRating.objects.filter(user__username=username, book__id=bookid):
            m_rating.rating = book_rating
            m_rating.save()
        return JsonResponse({'success': True, 'message': 'Rating has been updated'})
    else:
        instance = LibraryRating()
        instance.user = user
        instance.book = book
        instance.rating = book_rating
        instance.save()
        return JsonResponse({'success': True, 'message': 'Rating has been saved'})
