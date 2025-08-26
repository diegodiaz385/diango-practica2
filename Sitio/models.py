from django.db import models
from django.utils import timezone

# Create your models here.

class UserCredential(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    github_connected = models.BooleanField(default=False)
    github_username = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.email} - {'GitHub: ' + self.github_username if self.github_connected else 'Sin GitHub'}"
