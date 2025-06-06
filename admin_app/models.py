import datetime

from django.db import models
from django.db.models import Avg
from django.core.validators import FileExtensionValidator

from learningpost_professional.models import ProfessionalOrganization
from website.models import User


class Quest(models.Model):
    cover = models.ImageField(upload_to='quest_covers/')
    title = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, default='')
    time = models.IntegerField(verbose_name='Time per Question')
    about = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    bookmarked = models.ManyToManyField(User, blank=True)
    is_premium = models.BooleanField(default=False)
    organization = models.ForeignKey(ProfessionalOrganization, on_delete=models.CASCADE,
                                     related_name='professional_quests', null=True, blank=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.rated_quests.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 5.0


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
    topic = models.TextField(default='')
    is_draft = models.BooleanField(default=False)


class AnsweredBy(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='answered')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answered_by')
    date = models.DateField(auto_now_add=True)


class Library(models.Model):
    cover = models.ImageField(upload_to='book_covers/')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=200, null=True)
    about = models.TextField(blank=True, null=True)
    about_author = models.TextField(blank=True, null=True)
    bookmarked = models.ManyToManyField(User, blank=True)
    is_premium = models.BooleanField(default=False)
    organization = models.ForeignKey(ProfessionalOrganization, on_delete=models.CASCADE,
                                     related_name='professional_books', null=True, blank=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.rated_books.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 5.0


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    chapter_file = models.FileField(
        validators=[FileExtensionValidator(['epub'])], upload_to='chapters/')
    book = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name='chapters', null=True)

    def __str__(self):
        return self.title


class LibraryRating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='l_ratings')
    book = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name='rated_books')
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - Rating: {self.rating}"


class QuestRating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='q_ratings')
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, related_name='rated_quests')
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.quest.title} - Rating: {self.rating}"


class Leaderboard(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_rankings')
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, related_name='quest_rankings')
    streak = models.IntegerField(default=0)
    questions_answered = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.username} | {self.xp} xp | {self.date}"


class UserFeedback(models.Model):
    feedback_choices = [
        ('question_report', 'question_report'),
        ('help_desk', 'help_desk'),
        ('unsatisfied_user', 'unsatisfied_user'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='m_feedbacks', blank=True, null=True)
    message = models.TextField()
    is_viewed = models.BooleanField(default=False)
    feedback_type = models.CharField(
        max_length=20, choices=feedback_choices, null=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.feedback_type}\n{self.message}'


class MPerformance(models.Model):
    total_answered = models.IntegerField()
    correctly_answered = models.IntegerField()
    wrongly_answered = models.IntegerField()
    time = models.IntegerField(null=True)
    date = models.DateField()
    quest = models.ForeignKey(Quest, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='m_performance')

    def __str__(self):
        return f"{self.user.first_name} {self.date}"


class SubscriptionPlan(models.Model):
    currencies = [
        ('NGN', 'NGN'),
    ]
    plan = models.CharField(max_length=20)
    currency = models.CharField(max_length=5, choices=currencies, null=True)
    duration = models.IntegerField()
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.plan} ~ {self.price}'
