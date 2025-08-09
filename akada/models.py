import uuid
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


class GenerativeAIContentReport(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prompt = models.TextField()
    response = models.TextField()
    reason = models.CharField(max_length=255, help_text="User-provided reason for the report.")
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = 'Generative AI Content Report'
        verbose_name_plural = 'Generative AI Content Reports'

    def __str__(self):
        return f"Report #{self.conversation_id} by {self.reporter or 'Anonymous'}"
