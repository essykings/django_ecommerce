from .models import Cart
from django.db.models import Sum

def cart_items(request):
    if request.user.is_authenticated:
        customer = request.user
        total_cart_items = Cart.objects.filter(customer=customer).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    else:
        total_cart_items = 0
    return {'total_cart_items': total_cart_items}