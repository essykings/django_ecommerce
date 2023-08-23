from django.db import models
from store.models import Product
from django.conf import settings

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, null=False, blank=False)
    street_address = models.CharField(max_length=200,null=False, blank=False )
    city = models.CharField(max_length=200,null=False, blank=False) 
    house_number = models.CharField(max_length=200,null=False, blank=False) 
    other = models.CharField(max_length=200,null=True, blank=True) 
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100,null=True)
    SHIPPING_STATUS_CHOICES = (

        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        
    )
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    status = models.CharField(max_length=20, choices=SHIPPING_STATUS_CHOICES, default='Pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,   related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2, default= 0)

    def __str__(self):
        return str(self.order)
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity

    
class WishList(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='customer_wishlist')
    product = models.ForeignKey(Product, on_delete=   models.CASCADE,
               related_name='product_wishlist')

    def __str__(self):
        return str(self.product)
