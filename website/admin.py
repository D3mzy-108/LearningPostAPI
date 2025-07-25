from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name']


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    pass
