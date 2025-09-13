from django.db import models
from website.models import User


class ProfessionalOrganization(models.Model):
    organization_name = models.CharField(max_length=100)
    organization_logo = models.ImageField(
        upload_to='organization_logos/', null=True)
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
    pass_mark = models.FloatField(default=75.0)

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.question


class TestAttempt(models.Model):
    """Records a user's attempt at an exam."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    attempt_time = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True, default=0.0)
    is_voided = models.BooleanField(default=False)
    is_attempted = models.BooleanField(default=False)
    proctoring_failures = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name}'s attempt on {self.test.title}"

    @property
    def is_passed(self):
        """Determines if the attempt passed the test."""
        if self.score is not None and self.test.pass_mark is not None:
            return self.score >= self.test.pass_mark
        return False

    def to_json(self):
        return {
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
            },
            'test': {
                'id': self.test.id,
                'title': self.test.title,
                'expires': self.test.expires,
                'pass_mark': self.test.pass_mark,
            },
            'attempt_time': self.attempt_time,
            'score': self.score,
            'is_voided': self.is_voided,
            'is_attempted': self.is_attempted,
            'proctoring_failures': self.proctoring_failures,
            'is_passed': self.is_passed,
        }
