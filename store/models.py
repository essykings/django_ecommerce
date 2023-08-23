from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)
    

    @property
    def total_cost(self):
        total =0
        cart_total = self.product.price * self.quantity
        total +=cart_total
        return cart_total

    def __str__(self):
        return self.product.name