from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=220)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Purchase(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveBigIntegerField()
    total_price = models.PositiveBigIntegerField(blank=True)
    salesman = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self,*args, **kwargs):
        self.total_price = self.price*self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return f'sold {self.product} -{self.quantity} for {self.total_price}'
    
    
    
