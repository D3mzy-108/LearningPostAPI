from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('home/', about, name='about'),
    path('logout/', logout, name='logout'),
]
