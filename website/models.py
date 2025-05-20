from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    profile_photo = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    friends = models.ManyToManyField(
        'self', blank=True, symmetrical=False)
    dob = models.DateField(blank=True, null=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ~ {self.first_name}"

    def save(self, *args, **kwargs):
        if not self.username:
            usn_email = self.email.split('@')[0].lower()
            self.username = slugify(usn_email)
        super(User, self).save(*args, **kwargs)


class UserSubscription(models.Model):
    expiry_date = models.DateField()
    profile = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='subscription')
    is_confirmed = models.BooleanField(default=False)
    grades = models.TextField(default='', blank=True)

    def __str__(self):
        return f"{self.profile.first_name} -> {self.expiry_date}"
