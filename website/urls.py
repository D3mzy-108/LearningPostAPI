from django.urls import path
from .views import *

urlpatterns = [
    path('portal/login/', login, name='login'),
    path('', home, name='home'),
    path('terms-and-conditions/', ts_and_cs, name='tc'),
    path('privacy-policy/', pp, name='pp'),
    path('frequently-asked-questions/', faq, name='faq'),
    path('logout/', logout, name='logout'),
]
