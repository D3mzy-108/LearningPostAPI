from django.db import models
from website.models import User


class AkadaConversations(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='prompts')
    date = models.DateField(auto_now_add=True)
    prompt = models.TextField()
    system_response = models.TextField()

    class Meta:
        verbose_name = 'AkadaConversations'
        verbose_name_plural = 'AkadaConversations'

    def __str__(self):
        return f'{self.user.first_name} - {self.prompt}'


# from django.db import models


# class AkadaKnowledgeBank(models.Model):
#     content = models.TextField()

#     class Meta:
#         verbose_name = 'AkadaKnowledgeBank'
#         verbose_name_plural = 'AkadaKnowledgeBank'

#     def __str__(self):
#         return self.content[:30]
