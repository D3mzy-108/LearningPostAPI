from django.urls import path
from .views import get_challenge_questions, join_room, save_score


urlpatterns = [
    path('join/', join_room),
    path('questions/<int:testid>/<int:limit>/', get_challenge_questions),
    path('save-score/', save_score),
]
