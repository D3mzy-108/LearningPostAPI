from django.urls import path

from endpoints.api_views.subscription import get_subscription_plans, make_subscription_request, payment_success, subscribe

from .api_views.performance_views import get_performance, save_performance
from .api_views.auth_views import add_friend, login_endpoint, get_logged_in_user, edit_profile, update_status, request_account_deletion
from .api_views.quest_views import get_grades, get_practice_questions, get_quest, get_quest_topics, quests, questions, answer, rate_quest
from .api_views.library_views import library, chapters, rate_book
from .api_views.bookmarks_views import bookmarks, add_quest_to_bookmark, add_book_to_bookmark
from .api_views.leaderboard_views import get_top_10, get_top_10_global, update_rank
from .api_views.home_views import home_endpoint


urlpatterns = [
    # ========================================================================================================
    # AUTH
    # ========================================================================================================
    path('login/', login_endpoint),
    path('get-logged-in-user/<str:username>/', get_logged_in_user),
    path('edit-user-profile/<str:username>/', edit_profile),
    path('add-friend/<str:username>/', add_friend),
    path('update-status/', update_status),
    path('delete-account/', request_account_deletion),
    # ========================================================================================================
    # APPLICATION HOME PAGE
    # ========================================================================================================
    path('<str:username>/homepage/', home_endpoint),
    # ========================================================================================================
    # QUESTS
    # ========================================================================================================
    path('get-quests/<str:username>/', quests),
    path('get-quest-grades/', get_grades),
    path('get-quest/<int:testid>/<str:username>/', get_quest),
    path('quest/<int:testid>/get-questions/<str:username>/', questions),
    path('question/<str:questionids>/answered/<str:username>/', answer),
    path('<str:username>/rate-quest/<int:testid>/<str:rating>/', rate_quest),
    # PRACTICE QUEST
    path('get-quest-topics/<int:testid>/', get_quest_topics),
    path('get-practice-questions/<int:testid>/', get_practice_questions),
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
    path('top-ten-global-leaderboard/<str:username>/', get_top_10_global),
    path('update-rank/<str:username>/<int:testid>/', update_rank),
    # ========================================================================================================
    # PERFORMANCE
    # ========================================================================================================
    path('save-performance/<str:username>/', save_performance),
    path('get-performance/<str:username>/', get_performance),
    # ========================================================================================================
    # SUBSCRIPTION
    # ========================================================================================================
    path('subscription-plans/<str:username>/', get_subscription_plans),
    path('subscription/make-subscription-request/', make_subscription_request),
    path('subscription/subscribe/', subscribe),
    path('subscription/payment-success/', payment_success),
]
