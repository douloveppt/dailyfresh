from django.urls import path

from cart.views import *

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('add_cart/<int:id>/', add_cart, name='add_cart'),
    path('add_goods/<int:id>/', add_goods, name='add_goods'),
    path('minus_goods/<int:id>/', minus_goods, name='minus_goods'),
    path('del_goods/<int:id>/', del_goods, name='del_goods'),
]
