from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    # 'updated_at' is nullable and only set when an object is updated for the first time.
    # This helps distinguish between objects that have never been modified and those that have.
    # Potential issue: Setting 'updated_at' on new objects with a value different from 'created_at'
    # may give the impression that the object has been modified, even if it has not.
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]
