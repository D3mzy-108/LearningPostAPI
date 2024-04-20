from django.contrib import admin

from smartlink.models import SmartLinkKB


@admin.register(SmartLinkKB)
class SmartLinkKBAdmin(admin.ModelAdmin):
    list_per_page = 2000
