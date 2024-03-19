from django.contrib import admin

from smartlink.models import SmartLinkKB


@admin.register(SmartLinkKB)
class SmartLinkKBAdmin(admin.ModelAdmin):
    pass
