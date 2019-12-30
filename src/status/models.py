from django.conf import settings
from django.db import models
from django.contrib.auth.models import User



def upload_status_image(instance, filename):
    return f'updates/{instance.user}/{filename}'


class StatusQuerySet(models.QuerySet):
    pass


class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.models, using=self._db)


class Status(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_status_image, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # objects = StatusManager()
 
    def __str__(self):
        return str(self.content)[:50]

    class Meta:
        verbose_name = 'Status Post'
        verbose_name_plural = 'Status Posts'