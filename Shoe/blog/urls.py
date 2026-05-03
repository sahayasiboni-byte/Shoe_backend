from django.urls import path
from .views import get_users,create_user,login_user,add_to_cart,getcart_Userbyid,getcart_users,delete_cart


urlpatterns=[
    path('get',get_users,name='get'),
    path('register',create_user,name='register'),
    path('login',login_user,name='login'),
    path('cart/', add_to_cart, name='cart'),
    path('getaddcart/', getcart_users, name='getaddcart'),
    path('getcart/<int:id>/', getcart_Userbyid, name='getcart'),
    path('delete/<int:pk>',delete_cart,name='delete')
]

