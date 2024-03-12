from django.contrib import admin
from .models import ChallengeRoom, ChallengeScore


@admin.register(ChallengeRoom)
class ChallengeRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(ChallengeScore)
class ChallengeScoreAdmin(admin.ModelAdmin):
    pass
