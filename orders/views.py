from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Cart
from .forms import OrderForm,Order
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.views import View
from django.conf import settings
from .models import OrderItem
import stripe
from django.contrib.auth import get_user_model

User = get_user_model()




# class CreateCheckoutSessionView(View):
#     def get(self, request, *args, **kwargs):

#         # 
#         form = OrderForm()
#         cart_items = Cart.objects.filter(customer = request.user)
#         total_sum = sum(item.total_cost for item in cart_items)
#         context = {'form':form, 'cart_items':cart_items,'total_sum':total_sum}
#         return render(request,'orders/checkout.html', context )
    
#     @csrf_exempt
#     def post(self, request, *args, **kwargs):
#         cart_items = Cart.objects.filter(customer = request.user)
#         form = OrderForm(request.POST)
#         if form.is_valid():
#                 order = form.save(commit=False)
#                 order.customer = request.user
#                 order.save()

#                 for cart_item in cart_items:
#                     OrderItem.objects.create(
#                         order=order,
#                         product=cart_item.product,
#                         quantity=cart_item.quantity,
#                         price=cart_item.product.price,

#                     )
#         line_items =[]
#         for  item in cart_items:
#             line_items.append({
#                 'name':item.product.name,
#                 'quantity':item.quantity,
#                 'amount':int(item.product.price *100),
#                 'currency': 'usd',

#             })

        
#         return JsonResponse({'success':'order created'})

class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        form = OrderForm()
        cart_items = Cart.objects.filter(customer = request.user)
        total_sum = sum(item.total_cost for item in cart_items)
        context = {'form':form, 'cart_items':cart_items,'total_sum':total_sum}
        return render(request,'orders/checkout.html', context )
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = OrderForm()
        cart_items = Cart.objects.filter(customer = request.user)
        form = OrderForm(request.POST)
        if form.is_valid():
                order = form.save(commit=False)
                order.customer = request.user
                order.save()

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price,

                    )

        line_items =[]
        for  item in cart_items:
            line_items.append({
                'name':item.product.name,
                'quantity':item.quantity,
                'amount':int(item.product.price *100),
                'currency': 'usd',

            })
        
        domain_url = settings. DOMAIN_ROOT
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id,
            metadata = {'order_id':order.id},
            customer_email= request.user.email,
            success_url =domain_url+ 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + 'cancel/',
            payment_method_types=['card'],
            mode='payment',
            line_items = line_items,
                
            )
            
            request.session['checkout_session_id'] = checkout_session['id']
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error':str(e)})


def success_page(request):
    return render(request, 'success.html')


def cancelled_page(request):
    return render(request, 'cancelled.html')


from django.http import HttpResponse
from django.core.mail import send_mail
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload= request.body
    event = None
    sig_header = request.headers.get('stripe-signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status =400)
    # payment_intent.succeeded'
    if event['type'] == 'checkout.session.completed':
        payment_intent = event['data']['object']  
        print(payment_intent)
        
        user_id = payment_intent['client_reference_id']
        order_id = payment_intent['metadata']['order_id']
        
        order =  get_object_or_404(Order, id = order_id)
        order.payment_id = payment_intent['payment_intent']
        order.paid =True
        amount_total_dollars =  payment_intent['amount_total'] / 100
        order.amount = amount_total_dollars
        order.save()
        print(payment_intent['customer_email'])
       
        user = User.objects.get(id =user_id) 
        Cart.objects.filter(customer=user).delete()
    

        # TO DO : send email
        
        subject = 'Order Confirmation'
        message = f"Dear {user_id},\n\n" \
                  f"Your order of {order_id} has been confirmed. We will ship to you as soon as possible," \
                  "estimated delivery time is 3~8 days.\n\n" \
                  "Thank you for shopping with us!\n" \
                  "Best regards,\n" \
                  "The Lux Team"
        from_email = 'from@example.com'  
        recipient_list = [payment_intent['customer_email']]
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        

    return HttpResponse(status=200)

from django.views.generic import ListView

class OrderListView(ListView):
    template_name = 'orders/order_list.html'
    model = Order
    context_object_name = 'orders'
    paginate_by =20
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('date_created')
    
    
    
class OrderItemView(ListView):
    template_name = 'orders/order_detail.html'
    context_object_name = 'order_items_list'

    def get_queryset(self):
        order_id = self.kwargs['id']
        order = get_object_or_404(Order, id=order_id)
        return order.order_items.all()
        


from .models import WishList
def add_wishlist (request):
    """Add a product to the wishlist model"""

    if request.method =='POST':
        product_id = request.POST.get('id')
        wishlist = WishList.objects.filter(customer = request.user,product_id=product_id).exists()
        if not wishlist:
            wish = WishList(customer = request.user,product_id=product_id)
            wish.save()
        
    
    return redirect('/')

def wishlist (request):
    """Display all products in the wishlist for the logged in user"""

    wishlist = WishList.objects.filter(customer = request.user)
    context = {'wishlist':wishlist}
    return render(request,'orders/wish_list.html', context)