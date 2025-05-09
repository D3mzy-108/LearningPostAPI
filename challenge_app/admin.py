from django.contrib import admin
from .models import ArenaRoom, Participants


@admin.register(ArenaRoom)
class ArenaRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    pass
