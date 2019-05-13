from django.urls import path

from user.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('is_login/', is_login, name='is_login'),
    path('user_center_info/', user_center_info, name='user_center_info'),
    path('user_center_order/', user_center_order, name='user_center_order'),
    path('user_center_site/', user_center_site, name='user_center_site'),
    path('add_site/', add_site, name='add_site'),
]
