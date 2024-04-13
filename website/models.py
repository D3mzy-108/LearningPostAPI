from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    profile_photo = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ~ {self.first_name}"

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
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    guardian_email = models.EmailField(null=True, blank=True)
    guardian_phone = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class BetaReferal(models.Model):
    code = models.SlugField(unique=True)
    is_used = models.BooleanField(default=False)
    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='referral', blank=True, null=True)

    def __str__(self):
        return self.code


class SubAccounts(models.Model):
    parent = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sub_accounts')
    child = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.parent.first_name} -> {self.child.first_name}"


class UserSubscription(models.Model):
    expiry_date = models.DateField()
    support_quest = models.BooleanField(default=True)
    support_bookee = models.BooleanField(default=True)
    support_akada = models.BooleanField(default=True)
    supported_grades = models.TextField()
    profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='subscription')

    def __str__(self):
        return f"{self.profile.user.first_name} -> {self.expiry_date}"

    def get_grades(self):
        grades = self.supported_grades.split(' --- ')
        return grades


class SubscriptionLog(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='subscription_logs', null=True)
    code = models.SlugField(unique=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=5, null=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} >> {self.currency} {self.amount}"
