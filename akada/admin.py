from django.contrib import admin
from akada.models import AkadaKnowledgeBank


@admin.register(AkadaKnowledgeBank)
class AkadaKnowledgeBankAdmin(admin.ModelAdmin):
    pass
