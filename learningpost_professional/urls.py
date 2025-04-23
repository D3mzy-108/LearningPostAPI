from django.urls import path

from learningpost_professional.views import pro_quests

urlpatterns = [
    path('get-quests/<str:username>/', pro_quests),
]
