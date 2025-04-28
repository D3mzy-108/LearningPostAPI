from django.urls import path

from learningpost_professional.views import pro_library, pro_quests, professional_login, professional_signup

urlpatterns = [
    path('professional-signup/', professional_signup),
    path('professional-login/', professional_login),
    path('get-quests/<str:username>/', pro_quests),
    path('get-books/<str:username>/', pro_library),
]
