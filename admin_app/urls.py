from django.urls import path
from .views import *

urlpatterns = [
    # ========================================================================================================
    # QUESTS
    # ========================================================================================================
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
    # ========================================================================================================
    # CLASSIFICATIONS
    # ========================================================================================================
    path('classifications/', classifications, name="classifications"),
    path('classifications/generate-new-referral/',
         generate_new_code, name="generate_referral"),
    path('classifications/<int:id>/delete/', delete_code, name="delete_code"),
    # ========================================================================================================
    # LIBRARY
    # ========================================================================================================
    path('library/', library, name='library'),
    path('library/add/', create_book, name='create_book'),
    path('library/edit/<int:pk>/', edit_book, name='edit_book'),
    path('library/delete/<int:pk>/', delete_book, name='delete_book'),
    path('library/view/<int:pk>/chapters/', view_book, name='view_book'),
    path('library/view/<int:pk>/chapters/upload/',
         upload_chapter, name='upload_chapter'),
    path('library/chapter/delete/<int:pk>/',
         delete_chapter, name='delete_chapter'),
]
