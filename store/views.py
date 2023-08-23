from django.shortcuts import render,redirect
from .models import Product,Cart
from django.views.generic import ListView,DetailView
from .forms import CartForm
from django.db.models import Q 

class ProductListView(ListView):
    """Display all products"""

    model = Product
    template_name = 'store/product-list.html'
    context_object_name = 'products'

class productDetail(DetailView):
    """Display product detail and a cart Form"""
    model = Product
    template_name ='store/product_detail.html'
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CartForm()

        #check id product is in the cart
        product = self.get_object()
        cart_item = Cart.objects.filter(customer = self.request.user, product=product)
        if cart_item.exists():
            cart =cart_item.first()
        else:
            cart = None

        context['form'] = form
        context['cart'] = cart
        return context
    
def cart_add(request, product_id):
    """Add a product to the cart"""
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart = form.save(commit=False)
            cart.customer = request.user
            cart.product_id = product_id
            cart.save()

    return redirect('cart-list')

def cart_list(request):
    """retrieve cart items"""
    total_cost =0
    cartitems = Cart.objects.filter(customer=request.user)
    for item in cartitems:
        subtotal = item.total_cost
        total_cost+=subtotal
    
  
    context = {'cart_items':cartitems,'total_cost':total_cost }
    return render(request, 'store/cart_list.html', context) 

def update_cart_item(request):
    """Update cart quantities"""
    if request.method =='POST':
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('id')
        cart = Cart.objects.get(customer =request.user,product_id=product_id)
        cart.quantity=quantity
        cart.save()
    
    return redirect('cart-list')

def remove_cart_item (request):
    """Removes cart item from cart list"""
    if request.method =='POST':
        product_id = request.POST.get('id')
        cart = Cart.objects.get(customer =request.user,product_id=product_id)
        cart.delete()
    
    return redirect('cart-list')

def search(request):
    if request.method =='POST':
        query = request.POST.get('search','')
        products = Product.objects.filter(Q(name__icontains =query) | Q(description__icontains=query)) 
        print(products)
    return render(request, 'store/product_search.html', {'products': products})