from django.contrib import admin
from .models import *


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('quest__title', 'question', 'answered_by__user__username',
                     'answered_by__user__first_name',
                     'answered_by__date')


@admin.register(AnsweredBy)
class AnsweredByAdmin(admin.ModelAdmin):
    search_fields = ('user__username',
                     'user__first_name',
                     'date')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    pass


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestRating)
class QuestRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(LibraryRating)
class LibraryRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    pass


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    pass


@admin.register(MPerformance)
class MPerformanceAdmin(admin.ModelAdmin):
    pass
