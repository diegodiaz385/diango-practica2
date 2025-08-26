from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    github_username = models.CharField(max_length=100, blank=True, null=True)
    github_access_token = models.CharField(max_length=500, blank=True, null=True)
    github_avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.github_username}"

class SavedCredential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_credentials')
    service_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # En producción, esto debería estar encriptado
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'service_name', 'username']
    
    def __str__(self):
        return f"{self.user.username} - {self.service_name} - {self.username}"
