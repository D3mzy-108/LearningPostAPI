from django.contrib import admin
from akada.models import AkadaConversations, GeneratedStudyMaterials, GenerativeAIContentReport


@admin.register(AkadaConversations)
class AkadaConversationsAdmin(admin.ModelAdmin):
    list_display = ('date', 'prompt', 'user')
    list_filter = ('date',)
    readonly_fields = ('user', 'prompt', 'system_response', 'date')


@admin.register(GeneratedStudyMaterials)
class GeneratedStudyMaterialsAdmin(admin.ModelAdmin):
    list_display = ('topic', 'quest')
    search_fields = ('topic', 'quest__title')

@admin.register(GenerativeAIContentReport)
class GenerativeAIContentReportAdmin(admin.ModelAdmin):
    pass



# from django.contrib import admin
# from akada.models import AkadaKnowledgeBank


# @admin.register(AkadaKnowledgeBank)
# class AkadaKnowledgeBankAdmin(admin.ModelAdmin):
#     pass
