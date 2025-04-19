from django.contrib import admin
from akada.models import AkadaConversations, GeneratedStudyMaterials


@admin.register(AkadaConversations)
class AkadaConversationsAdmin(admin.ModelAdmin):
    list_display = ('date', 'prompt', 'user')
    list_filter = ('date',)


@admin.register(GeneratedStudyMaterials)
class GeneratedStudyMaterialsAdmin(admin.ModelAdmin):
    list_display = ('topic', 'quest')
    search_fields = ('topic', 'quest__title')


# from django.contrib import admin
# from akada.models import AkadaKnowledgeBank


# @admin.register(AkadaKnowledgeBank)
# class AkadaKnowledgeBankAdmin(admin.ModelAdmin):
#     pass
