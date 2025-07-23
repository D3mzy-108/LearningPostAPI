from django.urls import path

from admin_app.views import load_ext_form_data
from .admin_app_views.subscription_views import add_plan, modify_plan, plans, save_plan_instance
from .admin_app_views.quests_views import download_quest, quests, create_quest, edit_quest, delete_quest, submit_quest, view_questions, bulk_upload, single_upload, edit_question, delete_question
from .admin_app_views.library_views import create_book, delete_book, delete_chapter, edit_book, library, submit_book, upload_chapter, view_book
from .admin_app_views.reports_views import send_report, user_feedback

urlpatterns = [
    # ========================================================================================================
    # QUESTS
    # ========================================================================================================
    path('quests/', quests, name='quests'),
    path('ext-form-data/', load_ext_form_data, name='load_ext_form_data'),
    path('quests/save-instance/', submit_quest, name='submit_quest'),

#     path('quests/add/', create_quest, name='create_quest'),
#     path('quests/edit/<int:pk>/', edit_quest, name='edit_quest'),
#     path('quests/delete/<int:pk>/', delete_quest, name='delete_quest'),
    path('quests/<int:pk>/questions/', view_questions, name='view_questions'),
    path('quest/<int:testid>/questions/download/',
         download_quest, name='download_quest'),
    path('quests/<int:pk>/questions/upload/bulk/',
         bulk_upload, name='bulk_upload'),
    path('quests/<int:pk>/questions/upload/single/',
         single_upload, name='single_upload'),
    path('quests/<int:quest_pk>/questions/<int:pk>/edit/',
         edit_question, name='edit_question'),
    path('quests/questions/<int:pk>/delete/',
         delete_question, name='delete_question'),
    # ========================================================================================================
    # LIBRARY
    # ========================================================================================================
    path('library/', library, name='library'),
    path('library/save-instance/', submit_book, name='submit_book'),
    
#     path('library/add/', create_book, name='create_book'),
#     path('library/edit/<int:pk>/', edit_book, name='edit_book'),
#     path('library/delete/<int:pk>/', delete_book, name='delete_book'),
    path('library/view/<int:pk>/chapters/', view_book, name='view_book'),
    path('library/view/<int:pk>/chapters/upload/',
         upload_chapter, name='upload_chapter'),
    path('library/chapter/delete/<int:pk>/',
         delete_chapter, name='delete_chapter'),
    # ========================================================================================================
    # FEEDBACK & REPORTS
    # ========================================================================================================
    path('feedback/', user_feedback, name='user_feedback'),
    path('feedback/<str:username>/send/', send_report),
    # ========================================================================================================
    # SUBSCRIPTION PLANS
    # ========================================================================================================
    path('subscription-plans/', plans, name='subscription_plans'),
    path("subscription-plans/save-instance/", save_plan_instance, name="save_plan_instance"),
    path('subscription-plans/add/', add_plan, name='add_plan'),
    path('subscription-plans/<int:id>/modify/',
         modify_plan, name='modify_plan'),
]
