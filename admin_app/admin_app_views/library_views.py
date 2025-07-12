from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from ..models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# ========================================================================================================
# LIBRARY
# ========================================================================================================

def library(request):
    search = request.GET.get('search_books') or None
    books = Library.objects.filter(organization=None).order_by('-id')
    if search is not None:
        books = books.filter(title__icontains=search)
    paginator = Paginator(books, 50)
    page = request.GET.get('page')
    if page == None or int(page) > paginator.num_pages:
        page = 1
    displayed_books = paginator.page(page)

    context = {
        'success': True,
        'books': [
            {
                'id': book.pk,
                'cover': book.cover.url,
                'title': book.title,
                'author': book.author,
                'bookmark_count': book.bookmarked.count(),
                'chapter_count': book.chapters.count(),
                'rating': book.average_rating(),
                'about': book.about,
                'about_author': book.about_author,
                'organization': None,
                } for book in displayed_books
        ],
        'page': f'{page} of {displayed_books.paginator.num_pages}',
        'num_pages': displayed_books.paginator.num_pages,
        'search_val': search,
    }
    return JsonResponse(context)


@login_required
def create_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        try:
            cover = request.FILES.get('cover')
        except:
            return redirect('create_quest')
        about = request.POST['about']
        author = request.POST['author']
        about_author = request.POST['about_author']

        instance = Library()
        instance.title = title
        instance.cover = cover
        instance.about = about
        instance.author = author
        instance.about_author = about_author
        instance.is_premium = request.POST['is_premium'] == 'True'
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
        if request.POST['author'] is not None and request.POST['author'] != 'None':
            instance.about = request.POST['about']
            instance.author = request.POST['author']
            instance.about_author = request.POST['about_author']
            instance.is_premium = request.POST['is_premium'] == 'True'
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
        'chapters': book.chapters.all().order_by('title'),
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
