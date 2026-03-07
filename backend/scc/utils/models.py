from django.db import models

from scc.utils.managers import ActiveManager, AllObjectsManager


class ActiveModel(models.Model):
    active = models.BooleanField(default=True)  # type: ignore[arg-type]

    objects = AllObjectsManager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
