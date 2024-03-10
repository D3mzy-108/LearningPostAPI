from django.urls import path
from .views import create_room, delete_room, get_challenge_questions, join_room, save_score


urlpatterns = [
    path('create/', create_room),
    path('join/', join_room),
    path('delete/<slug:slug>/', delete_room),
    path('questions/<int:testid>/<int:limit>/', get_challenge_questions),
    path('save-score/', save_score),
]
