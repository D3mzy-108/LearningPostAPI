from django.urls import path

from learningpost_professional.views import (get_questions, get_score, get_tests, pro_library,
                                             pro_quests, professional_login, professional_signup, save_test_score, join_organization)

urlpatterns = [
    path('professional-signup/', professional_signup),
    path('professional-login/', professional_login),
    path('join-organization/', join_organization),
    path('get-quests/<str:username>/', pro_quests),
    path('get-books/<str:username>/', pro_library),
    path('get-tests/<str:username>/', get_tests),
    path('get-test-questions/<int:testid>/', get_questions),
    path('save-score/<str:username>/<int:testid>/', save_test_score),
    path('get-score/<str:username>/<int:testid>/', get_score),
]
