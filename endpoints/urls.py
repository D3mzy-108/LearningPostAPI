from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('get-quests/', quests),
    path('quest/<int:testid>/get-questions/', questions),
    path('question/<int:questionid>/answered/', answer),
]
