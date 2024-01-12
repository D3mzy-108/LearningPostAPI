from django.urls import path
from .views import *

urlpatterns = [
    path('quests/', quests, name='quests'),
    path('quests/add/', create_quest, name='create_quest'),
    path('quests/edit/<int:pk>/', edit_quest, name='edit_quest'),
    path('quests/delete/<int:pk>/', delete_quest, name='delete_quest'),
    path('quests/<int:pk>/questions/', view_questions, name='view_questions'),
    path('quests/<int:pk>/questions/upload/bulk/',
         bulk_upload, name='bulk_upload'),
    path('quests/<int:pk>/questions/upload/single/',
         single_upload, name='single_upload'),
    path('quests/<int:quest_pk>/questions/<int:pk>/edit/',
         edit_question, name='edit_question'),
    path('quests/questions/<int:pk>/delete/',
         delete_question, name='delete_question'),
]
