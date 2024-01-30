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


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestRating)
class QuestRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(LibraryRating)
class LibraryRatingAdmin(admin.ModelAdmin):
    pass
