from django.urls import path
from akada.views import (
    prompt_akada,
    flag_ai_response,
    request_smartlink,
    get_study_materials,
    get_material_content,
    bookmark_study_material,
)
# from .views import akada_home, chat_with_akada

urlpatterns = [
    path('chat/<str:username>/', prompt_akada),
    path('smartlink/<str:username>/', request_smartlink),
    # STUDY MATERIALS URLS
    path('get-study-materials/', get_study_materials),
    path('get-material-content/<int:material_id>/', get_material_content),
    path('bookmark-study-material/<int:material_id>/<str:username>/',
         bookmark_study_material),
    path('flag-ai-response/', flag_ai_response, name='flag_ai_response')
    #     path('', akada_home, name='akada_home'),
    #     path('chat/<str:username>/', chat_with_akada, name='chat_with_akada'),
]
