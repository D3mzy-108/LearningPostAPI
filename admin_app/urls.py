from django.urls import path
from .admin_app_views.quests_views import quests, create_quest, edit_quest, delete_quest, view_questions, bulk_upload, single_upload, edit_question, delete_question
from .admin_app_views.library_views import create_book, delete_book, delete_chapter, edit_book, library, upload_chapter, view_book
from .admin_app_views.classifications_views import classifications, delete_code, generate_new_code
from .admin_app_views.reports_views import user_feedback

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
    # ========================================================================================================
    # FEEDBACK & REPORTS
    # ========================================================================================================
    path('feedback/', user_feedback, name='user_feedback'),
]
