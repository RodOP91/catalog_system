from django.db import models
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    sku= models.CharField(max_length=16, unique=True)
    name= models.CharField(max_length=100)
    brand= models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    query_count= models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} ({self.brand})"

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

