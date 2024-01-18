from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_endpoint),
    path('get-quests/<str:username>/', quests),
    path('quest/<int:testid>/get-questions/<str:username>/', questions),
    path('question/<int:questionid>/answered/<str:username>/', answer),
    path('get-bookmarks/<str:username>/', bookmarks),
    path('add-to-bookmarks/<str:username>/<int:testid>/<str:is_adding>/',
         add_to_bookmark),
]
