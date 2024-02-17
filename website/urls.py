from django.urls import path
from .views import *

urlpatterns = [
    path('portal/login/', home, name='home'),
    path('', about, name='about'),
    path('logout/', logout, name='logout'),
]
