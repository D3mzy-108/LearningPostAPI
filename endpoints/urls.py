from django.urls import path
from .views import *

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
]
