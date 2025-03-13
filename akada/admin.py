from django.contrib import admin
from akada.models import AkadaConversations


@admin.register(AkadaConversations)
class AkadaConversationsAdmin(admin.ModelAdmin):
    list_display = ('date', 'prompt', 'user')
    list_filter = ('date',)


# from django.contrib import admin
# from akada.models import AkadaKnowledgeBank


# @admin.register(AkadaKnowledgeBank)
# class AkadaKnowledgeBankAdmin(admin.ModelAdmin):
#     pass
