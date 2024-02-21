from django.urls import path
from .views import *

urlpatterns = [
    path('portal/login/', home, name='home'),
    path('', about, name='about'),
    path('terms-and-conditions/', ts_and_cs),
    path('privacy-policy/', pp),
    path('frequently-asked-questions/', faq),
    path('logout/', logout, name='logout'),
]
