from django.urls import path
from akada.views import prompt_akada, request_smartlink
# from .views import akada_home, chat_with_akada

urlpatterns = [
    path('chat/<str:username>/', prompt_akada),
    path('smartlink/<str:username>/', request_smartlink),
    #     path('', akada_home, name='akada_home'),
    #     path('chat/<str:username>/', chat_with_akada, name='chat_with_akada'),
]
