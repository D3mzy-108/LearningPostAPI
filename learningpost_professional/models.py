from django.db import models

from website.models import User


class ProfessionalOrganization(models.Model):
    organization_name = models.CharField(max_length=100)
    organization_code = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User, blank=True, null=True)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.organization_name
