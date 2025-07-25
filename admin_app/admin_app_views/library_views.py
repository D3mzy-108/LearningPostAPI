from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from ..models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


# ========================================================================================================
# LIBRARY
# ========================================================================================================
def _build_book_object(book):
    return {
        'id': book.pk,
        'cover': book.cover.url,
        'title': book.title,
        'author': book.author,
        'bookmark_count': book.bookmarked.count(),
        'chapter_count': book.chapters.count(),
        'rating': book.average_rating(),
        'about': book.about,
        'about_author': book.about_author,
        'organization': book.organization.organization_code if book.organization else None,
    }

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
            _build_book_object(book) for book in displayed_books
        ],
        'page': f'{page} of {displayed_books.paginator.num_pages}',
        'num_pages': displayed_books.paginator.num_pages,
        'search_val': search,
    }
    return JsonResponse(context)


@require_POST
@csrf_exempt
def submit_book(request):
    book_id = request.POST.get('id')
    title = request.POST['title']
    cover = request.FILES.get('cover')
    about = request.POST['about']
    author = request.POST['author']
    about_author = request.POST['about_author']
    organization_code = request.POST.get('organization_code', None)

    if organization_code:
        organization = get_object_or_404(
            ProfessionalOrganization, organization_code=organization_code)
    else:
        organization = None

    if book_id == None or book_id == '':
        Library.objects.create(
            title = title,
            cover = cover,
            about = about,
            author = author,
            about_author = about_author,
            organization=organization,
        )
    else:
        instance = get_object_or_404(Library, pk=book_id)
        instance.title = request.POST['title']
        cover = request.FILES.get('cover')
        if cover is not None:
            instance.cover = cover
        instance.about = about
        instance.author = author
        instance.about_author = about_author
        instance.organization = organization
        instance.save()
    return JsonResponse({'success': True, 'message': 'Book saved successfully'})


def view_book(request, pk):
    book = get_object_or_404(Library, pk=pk)
    context = {
        'success': True,
        'book': _build_book_object(book),
        'chapters': [
            {
                'id': chapter.pk,
                'title': chapter.title,
            } for chapter in book.chapters.all().order_by('title')
        ],
    }
    return JsonResponse(context)


@require_POST
@csrf_exempt
def upload_chapter(request, pk):
    chapter = Chapter()
    chapter.title = request.POST.get('title')
    chapter.chapter_file = request.FILES.get('chapter')
    chapter.book = get_object_or_404(Library, pk=pk)
    chapter.save()
    return JsonResponse({'success': True, 'message': 'Chapter saved!'})


def delete_chapter(request, pk):
    get_object_or_404(Chapter, pk=pk).delete()
    return JsonResponse({'success': True, 'message': 'Chapter deleted!'})
