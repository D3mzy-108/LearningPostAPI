from django.urls import path

from learningpost_professional.certification_exam.views import certification_test_list, get_attempt, save_test_score, start_test
from learningpost_professional.views import (get_learning_tracks, pro_library,
                                             pro_quests, professional_login, professional_signup, add_learning_track, update_pro_user_profile)

urlpatterns = [
    path('professional-signup/', professional_signup),
    path('professional-login/', professional_login),
    path('user-profile/update/', update_pro_user_profile),
    path('add-learning-track/', add_learning_track),
    path('get-learning-tracks/<str:username>/', get_learning_tracks),
    path('get-quests/<str:username>/', pro_quests),
    path('get-books/<str:username>/', pro_library),
    path('get-tests/<str:username>/', certification_test_list),
    path('start-test/<int:test_id>/<str:username>/', start_test),
    path('save-test-score/<str:username>/<int:testid>/', save_test_score),
    path('get-test-attempt/<str:username>/<int:testid>/', get_attempt),
]
