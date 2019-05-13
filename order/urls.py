from django.urls import path

from order.views import *

urlpatterns = [
    path('order/', order, name='order'),
]
