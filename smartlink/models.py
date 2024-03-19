from django.db import models


class SmartLinkKB(models.Model):
    statement = models.TextField()
    definition = models.TextField()

    class Meta:
        verbose_name = 'SmartLinkKB'
        verbose_name_plural = 'SmartLinksKB'

    def __str__(self):
        return self.statement
