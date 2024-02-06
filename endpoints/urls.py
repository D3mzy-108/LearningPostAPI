from django.urls import path
from .api_views.auth_views import login_endpoint, get_logged_in_user, edit_profile
from .api_views.quest_views import quests, questions, answer
from .api_views.library_views import library, chapters
from .api_views.bookmarks_views import bookmarks, add_quest_to_bookmark, add_book_to_bookmark


urlpatterns = [
    # ========================================================================================================
    # AUTH
    # ========================================================================================================
    path('login/', login_endpoint),
    path('get-logged-in-user/<str:username>/', get_logged_in_user),
    path('edit-user-profile/<str:username>/', edit_profile),
    # ========================================================================================================
    # QUESTS
    # ========================================================================================================
    path('get-quests/<str:username>/', quests),
    path('quest/<int:testid>/get-questions/<str:username>/', questions),
    path('question/<int:questionid>/answered/<str:username>/', answer),
    # ========================================================================================================
    # LIBRARY
    # ========================================================================================================
    path('get-books/<str:username>/', library),
    path('<str:username>/book/<int:bookid>/chapters/', chapters),
    # ========================================================================================================
    # BOOKMARKS
    # ========================================================================================================
    path('get-bookmarks/<str:username>/', bookmarks),
    path('add-quest-to-bookmarks/<str:username>/<int:testid>/<str:is_adding>/',
         add_quest_to_bookmark),
    path('add-book-to-bookmarks/<str:username>/<int:bookid>/<str:is_adding>/',
         add_book_to_bookmark),
]
