from django.urls import path

from goods.views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('detail/<int:id>/', detail, name='detail'),
    path('goods_list/<int:id>/', goods_list, name='goods_list'),
]
