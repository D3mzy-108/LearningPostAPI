from django.contrib import admin
from .models import ChallengeRoom


@admin.register(ChallengeRoom)
class ChallengeRoomAdmin(admin.ModelAdmin):
    pass
