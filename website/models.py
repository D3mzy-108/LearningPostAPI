from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    profile_photo = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            usn_email = self.email.split('@')[0].lower()
            self.username = slugify(usn_email)
        super(User, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    school = models.TextField(null=True, blank=True)
    referal_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    guardian_email = models.EmailField(null=True, blank=True)
    guardian_phone = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
