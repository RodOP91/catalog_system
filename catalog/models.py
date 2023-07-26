from django.db import models

class Product(models.Model):
    sku= models.CharField(max_length=16, unique=True)
    name= models.CharField(max_length=100)
    brand= models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    query_count= models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} ({self.brand})"

class PriceList(models.Model):
    name= models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

class ProductPriceList(models.Model):
    price_list_id = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    
    class Meta:
        unique_together = ('product_id', 'price_list_id')