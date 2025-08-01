from django.contrib import admin

from learningpost_professional.models import ProfessionalOrganization, Score, Test, TestQuestion


@admin.register(ProfessionalOrganization)
class ProfessionalOrganizationAdmin(admin.ModelAdmin):
    pass
    # list_display = ('',)
    # list_filter = ('',)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    pass
