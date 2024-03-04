from django.db import models
from website.models import User


class ChallengeRoom(models.Model):
    room_name = models.SlugField(unique=True)
    no_of_rounds = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

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
    score = models.IntegerField(default=0)
