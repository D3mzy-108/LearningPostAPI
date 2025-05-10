from django.urls import path
from .views import change_quest, get_challenge_questions, join_room, save_score


urlpatterns = [
    path('join/', join_room),
    path('change-quest/', change_quest),
    path('questions/<int:testid>/<int:limit>/', get_challenge_questions),
    path('save-score/', save_score),
]
