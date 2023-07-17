from django.db import models

class Product(models.Model):
    sku= models.CharField(max_length=16, unique=True)
    name= models.CharField(max_length=100)
    brand= models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    query_count= models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} ({self.brand})"
