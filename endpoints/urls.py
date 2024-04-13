from django.urls import path

from .api_views.performance_views import get_challenge_performance, get_performance, save_performance
from .api_views.auth_views import add_sub_account, log_subscription, login_endpoint, get_logged_in_user, edit_profile, get_plans, subscription_success
from .api_views.quest_views import get_grades, get_quest, quests, questions, answer, rate_quest
from .api_views.library_views import library, chapters, rate_book
from .api_views.bookmarks_views import bookmarks, add_quest_to_bookmark, add_book_to_bookmark
from .api_views.leaderboard_views import get_top_10, update_rank


urlpatterns = [
    # ========================================================================================================
    # AUTH
    # ========================================================================================================
    path('login/', login_endpoint),
    path('get-logged-in-user/<str:username>/', get_logged_in_user),
    path('edit-user-profile/<str:username>/', edit_profile),
    path('add-sub-account/<str:username>/', add_sub_account),
    path('subscription-plans/', get_plans),
    path('log-subscription/', log_subscription),
    path('subscription-success/<str:username>/<int:quest_support>/<int:bookee_support>/<int:akada_support>/<str:selected_grades>/<int:duration>/', subscription_success),
    # ========================================================================================================
    # QUESTS
    # ========================================================================================================
    path('get-quests/<str:username>/', quests),
    path('get-quest-grades/', get_grades),
    path('get-quest/<int:testid>/<str:username>/', get_quest),
    path('quest/<int:testid>/get-questions/<str:username>/', questions),
    path('question/<str:questionids>/answered/<str:username>/', answer),
    path('<str:username>/rate-quest/<int:testid>/<str:rating>/', rate_quest),
    # ========================================================================================================
    # LIBRARY
    # ========================================================================================================
    path('get-books/<str:username>/', library),
    path('<str:username>/book/<int:bookid>/chapters/', chapters),
    path('<str:username>/rate-book/<int:bookid>/<str:rating>/', rate_book),
    # ========================================================================================================
    # BOOKMARKS
    # ========================================================================================================
    path('get-bookmarks/<str:username>/', bookmarks),
    path('add-quest-to-bookmarks/<str:username>/<int:testid>/<str:is_adding>/',
         add_quest_to_bookmark),
    path('add-book-to-bookmarks/<str:username>/<int:bookid>/<str:is_adding>/',
         add_book_to_bookmark),
    # ========================================================================================================
    # LEADERBOARD
    # ========================================================================================================
    path('top-ten-leaderboard/<str:username>/<int:testid>/', get_top_10),
    path('update-rank/<str:username>/<int:testid>/', update_rank),
    # ========================================================================================================
    # PERFORMANCE
    # ========================================================================================================
    path('save-performance/<str:username>/', save_performance),
    path('get-performance/<str:username>/', get_performance),
    path('get-challenge-history/<str:username>/', get_challenge_performance),
]
