from django.db import models 
from django.conf import settings 

class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    parent = models.ForeignKey('self',on_delete = models.SET_NULL,null=True,blank=True,related_name="subcategories")
    
    def __str__(self):
           return self.name 

class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name = "product")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='products/',blank=True,null=True)
    status = models.CharField(
        max_length = 20,
        choices = [("available", "Available"),("out_of_stock","Out of stock"), ("discontinued","Discontinued")],
        default = "available"
        )
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} - {self.seller.email}"
