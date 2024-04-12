from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(BetaReferal)
class BetaReferalAdmin(admin.ModelAdmin):
    pass


@admin.register(SubAccounts)
class SubAccountsAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(SubscriptionLog)
class SubscriptionLogAdmin(admin.ModelAdmin):
    pass
