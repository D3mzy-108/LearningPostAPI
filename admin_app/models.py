from django.db import models
from django.db.models import Avg
from website.models import User
from django.core.validators import FileExtensionValidator


class Quest(models.Model):
    quest_types = [
        ('mc', 'Multi-choice'),
        ('th', 'Theory'),
    ]
    cover = models.ImageField(upload_to='quest_covers/')
    title = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    time = models.IntegerField(verbose_name='Time per Question')
    about = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    quest_type = models.CharField(max_length=100, choices=quest_types)
    bookmarked = models.ManyToManyField(User, blank=True)

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


class AnsweredBy(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='answered')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answered_by')
    date = models.DateField(auto_now_add=True)


class Library(models.Model):
    cover = models.ImageField(upload_to='book_covers/')
    title = models.CharField(max_length=100)
    about = models.TextField(blank=True, null=True)
    about_author = models.TextField(blank=True, null=True)
    bookmarked = models.ManyToManyField(User, blank=True)

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
