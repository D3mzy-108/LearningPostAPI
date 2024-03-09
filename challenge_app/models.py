from django.db import models
from website.models import User
from django.utils.text import slugify
from admin_app.models import Quest


class ChallengeRoom(models.Model):
    room_name = models.CharField(max_length=20)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    room_slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.room_slug = slugify(self.room_name)
        super(ChallengeRoom, self).save(*args, **kwargs)

    def __str__(self):
        if self.is_active:
            is_active_str = 'Active'
        else:
            is_active_str = 'Inactive'
        return f'{self.room_name} {is_active_str}'


class ChallengeScore(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='challenges')
    room = models.ForeignKey(
        ChallengeRoom, on_delete=models.CASCADE, related_name='scores')
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    score_3 = models.IntegerField(default=0)
    score_4 = models.IntegerField(default=0)
    score_5 = models.IntegerField(default=0)
