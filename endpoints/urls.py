from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_endpoint),
    path('get-quests/', quests),
    path('quest/<int:testid>/get-questions/', questions),
    path('question/<int:questionid>/answered/', answer),
    path('get-bookmarks/', bookmarks),
    path('add-to-bookmarks/<int:testid>/<str:is_adding>/', add_to_bookmark),
]
