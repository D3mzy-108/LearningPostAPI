from django.db import models


class AkadaKnowledgeBank(models.Model):
    content = models.TextField()

    class Meta:
        verbose_name = 'AkadaKnowledgeBank'
        verbose_name_plural = 'AkadaKnowledgeBank'

    def __str__(self):
        return self.content[:30]
