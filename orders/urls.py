from django.urls import path
from . import views 
urlpatterns = [
  
  
    path('checkout',views.CreateCheckoutSessionView.as_view(), name='checkout' ),
    path('success',views.success_page, name='success' ),
    path('cancel',views.cancelled_page, name='cancel' ),
    path('webhooks',views.stripe_webhook, name='webhooks' ),
    path('orders',views.OrderListView.as_view(), name='orders' ),
    path('orders/<int:id>/', views.OrderItemView.as_view(), name='order-detail'),

  path('add_wish',views.add_wishlist, name='add-wish' ), #new
    path('wishlist',views.wishlist, name='wishlist' ),
]