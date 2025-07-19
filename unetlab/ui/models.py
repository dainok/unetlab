from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model extending default Django User."""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
