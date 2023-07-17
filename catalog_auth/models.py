import secrets

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='catalog_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='catalog_users', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class AuthToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auth_token')
    token = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def save(self, *args, **kwargs):
        token_value = secrets.token_hex(15) 
        if not self.pk:
            self.token = token_value
            if not self.expires_at:
                self.expires_at = timezone.now() + timezone.timedelta(days=1)
        return super().save(*args, **kwargs)
    
    def get_token(self):
        return self.token
