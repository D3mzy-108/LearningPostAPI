from django.db import models
from website.models import User


class Quest(models.Model):
    quest_types = [
        ('mc', 'Multi-choice'),
        ('th', 'Theory'),
    ]
    cover = models.ImageField(upload_to='quest_covers/')
    title = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    time = models.IntegerField(verbose_name='Time per Question')
    instructions = models.TextField(blank=True, null=True)
    quest_type = models.CharField(max_length=100, choices=quest_types)
    bookmarked = models.ManyToManyField(User, blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, related_name='questions')
    comprehension = models.TextField(blank=True, null=True)
    diagram = models.ImageField(upload_to='diagrams/', blank=True, null=True)
    question = models.TextField()
    a = models.TextField()
    b = models.TextField()
    c = models.TextField()
    d = models.TextField()
    answer = models.TextField()
    explanation = models.TextField()


class AnsweredBy(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='answered')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answered_by')
    date = models.DateField(auto_now_add=True)
