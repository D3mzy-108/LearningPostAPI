import random
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from admin_app.models import *
from django.db.models import Avg, ExpressionWrapper, fields

from admin_app.utils.grades import user_subscribed_grades


def _get_quest(username):
    user = get_object_or_404(User, username=username)
    grades = user_subscribed_grades(user)
    if len(grades) == 0:
        quests = Quest.objects.filter(organization=None).order_by('?')
    else:
        quests = Quest.objects.filter(
            grade__in=grades, organization=None).order_by('?')
    paginator = Paginator(quests, 20)
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
            'isPremium': quest.is_premium,
            'time': quest.time,
            'about': quest.about,
            'instructions': quest.instructions,
            'bookmarked': quest.bookmarked.filter(username=username).exists(),
            'question_count': quest.questions.count(),
            'answered_count': answered_count,
            'rating': rating,
        })
    grade_list = Quest.objects.all().order_by(
        'grade').values_list('grade', flat=True).distinct()
    category_list = Quest.objects.all().order_by(
        'category').values_list('category', flat=True).distinct()
    list_of_grades = []
    list_of_categories = []
    for grade in grade_list:
        list_of_grades.append(grade)
    for category in category_list:
        list_of_categories.append(category)
    return quests_list


def _get_book(username):
    books = Library.objects.filter(organization=None).order_by('?')
    paginator = Paginator(books, 20)
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
            'author': book.author,
            'about_author': book.about_author,
            'isPremium': book.is_premium,
            'bookmarked': book.bookmarked.filter(username=username).exists(),
            'chapters_count': Chapter.objects.filter(book__id=book.id).count(),
            'rating': rating,
        })
    return books_list


def home_endpoint(request, username):
    section_titles = [
        {
            "type": "QUEST",
            "titles": [
                "Time to Play!",
                "Ready to Play?",
                "Let's Do This!",
                "It's Game Time!",
                "Fun Stuff to Do!",
                "Adventures Await!",
                "Embark on Quests!",
                "Let's Get Started!",
                "Challenge Accepted!",
                "Interact and Explore!",
                "Let's Get Adventuring!",
                "What Can You Do Today?",
                "Ready for a Challenge?",
                "What Will You Discover?",
                "Unleash Your Inner Guru!",
            ],
        },
        {
            "type": "BOOKEE",
            "titles": [
                "Happy Reading!",
                "Let's Get Lit!",
                "Handpicked Reads!",
                "Dive into a Story!",
                "Books Just for You!",
                "Explore New Worlds!",
                "Get Lost in a Book!",
                "Fuel Your Curiosity!",
                "Fuel Your Imagination!",
                "Time to Relax and Read!",
                "What Will You Read Next?",
                "Personalized Reading List!",
                "Unleash Your Inner Bookworm!",
                "Your Next Great Read Awaits!",
                "Let's Find Your Perfect Book!",
            ],
        },
    ]
    home_sections = []
    for section in section_titles:
        if section.get('type') == 'QUEST':
            title = random.choice(section.get('titles'))
            section_content = _get_quest(username)
        elif section.get('type') == 'BOOKEE':
            title = random.choice(section.get('titles'))
            section_content = _get_book(username)
        home_sections.append({
            'title': title,
            'type': section.get('type'),
            'content': section_content,
        })
    return JsonResponse({
        'success': True,
        'sections': home_sections,
    })
