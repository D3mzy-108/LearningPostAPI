from django.db import models


class AkadaKnowledgeBank(models.Model):
    file_path = models.CharField(max_length=300)
    content = models.TextField()

    class Meta:
        verbose_name = 'AkadaKnowledgeBank'
        verbose_name_plural = 'AkadaKnowledgeBank'

    def __str__(self):
        return self.file_path
