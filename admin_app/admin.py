from django.contrib import admin
from .models import *


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(AnsweredBy)
class AnsweredByAdmin(admin.ModelAdmin):
    pass
