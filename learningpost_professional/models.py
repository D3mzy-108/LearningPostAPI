from django.db import models
from django.db.models import Avg

from website.models import User


class ProfessionalOrganization(models.Model):
    organization_name = models.CharField(max_length=100)
    organization_code = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.organization_name


class Test(models.Model):
    cover = models.ImageField(upload_to='quest_covers/')
    title = models.CharField(max_length=100)
    time = models.IntegerField(verbose_name='Time per Question')
    about = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(ProfessionalOrganization, on_delete=models.CASCADE,
                                     related_name='professional_tests', null=True, blank=True)
    expires = models.DateField()

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.rated_quests.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 5.0


class TestQuestion(models.Model):
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='test_questions')
    comprehension = models.TextField(blank=True, null=True)
    diagram = models.ImageField(upload_to='diagrams/', blank=True, null=True)
    question = models.TextField()
    a = models.TextField()
    b = models.TextField()
    c = models.TextField()
    d = models.TextField()
    answer = models.TextField()


class Score(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='test_scores')
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='participants')
    score = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Score'
        verbose_name_plural = 'Scores'

    def __str__(self):
        pass
