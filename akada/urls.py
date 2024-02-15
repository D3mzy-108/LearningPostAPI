from django.urls import path
from .views import akada_home, chat_with_akada

urlpatterns = [
    path('', akada_home, name='akada_home'),
    path('chat/', chat_with_akada, name='chat_with_akada'),
]
