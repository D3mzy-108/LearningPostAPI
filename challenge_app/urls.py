from django.urls import path
from .views import challenge_history, change_quest, get_challenge_questions, get_participants, join_room, leave_arena, save_score


urlpatterns = [
    path('join/', join_room),
    path('change-quest/', change_quest),
    path('questions/<int:testid>/<int:limit>/', get_challenge_questions),
    path('save-score/', save_score),
    path('get-participants/<str:room_name>/<str:username>/', get_participants),
    path('leave-arena/<str:room_name>/', leave_arena),
    path('history/', challenge_history),
]
