from django.db import models
from admin_app.models import Quest
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


class GeneratedStudyMaterials(models.Model):
    quest = models.ForeignKey(
        Quest, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    bookmarked = models.ManyToManyField(
        User, related_name='bookmarked_study_materials', blank=True)

    class Meta:
        verbose_name = 'GeneratedStudyMaterials'
        verbose_name_plural = 'GeneratedStudyMaterials'

    def __str__(self):
        return f'{self.topic}'

    # def save(self, *args, **kwargs):
    #     is_new_instance = self._state.adding
    #     if is_new_instance:
    #         if self.quest is not None and not self.quest.title in self.topic:
    #             self.topic = f'{self.topic}'
    #     return super().save(*args, **kwargs)


# from django.db import models


# class AkadaKnowledgeBank(models.Model):
#     content = models.TextField()

#     class Meta:
#         verbose_name = 'AkadaKnowledgeBank'
#         verbose_name_plural = 'AkadaKnowledgeBank'

#     def __str__(self):
#         return self.content[:30]
