from django.urls import path
from .views import bulk_upload_smartlinks, smartlinks


urlpatterns = [
    path('', smartlinks, name='smartlinks'),
    path('bulk-upload/', bulk_upload_smartlinks, name='bulk_upload_smartlinks'),
]
