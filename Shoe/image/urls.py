from django.urls import path
from .views import get_images,create_images,create_product,get_product,get_Userbyid,get_last_8_products
urlpatterns=[
    path('get',get_images,name='get'),
    path('create',create_images,name='create'),
    path('createproduct',create_product,name='createproduct'),
    path('getproduct',get_product,name='getproduct'),
    path('get_product/<int:pk>',get_Userbyid,name='get_userbyid'),
    path('last',get_last_8_products,name='last'),
    
]