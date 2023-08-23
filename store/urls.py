from django.urls import path
from . import views 


urlpatterns = [
   
    path('',views.ProductListView.as_view(), name='product-list' ),
    path('<int:pk>',views.productDetail.as_view(), name='product-detail' ),
    path('cart_add/<int:product_id>',views.cart_add, name='cart-add' ), 
    path('cart_list',views.cart_list, name='cart-list' ), 
    path('update_item',views.update_cart_item, name='update-item' ), 
    path('remove_item',views.remove_cart_item, name='remove-item' ), 
    path('search',views.search, name='search' ), #new
    
    ]