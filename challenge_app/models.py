from django.db import models
from website.models import User
from django.utils.text import slugify
from admin_app.models import Quest


class ArenaRoom(models.Model):
    room_name = models.CharField(max_length=20)
    quest = models.ForeignKey(
        Quest, on_delete=models.CASCADE, null=True, blank=True)
    questions = models.IntegerField(default=20)
    time = models.IntegerField(default=15)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    room_slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.room_slug = slugify(self.room_name)
        super(ArenaRoom, self).save(*args, **kwargs)

    def __str__(self):
        if self.is_active:
            is_active_str = 'Active'
        else:
            is_active_str = 'Inactive'
        return f'{self.room_name} {is_active_str}'


class Participants(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='challenges')
    room = models.ForeignKey(
        ArenaRoom, on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField(default=0)
