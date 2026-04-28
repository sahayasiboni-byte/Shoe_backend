from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import img,products
from .serializer import MediaFileSerializer ,ProductFileSerializer,productSerializer
import re
# Create your views here.
@api_view(['GET']) #method type
def get_images(request):
    users=img.objects.all()
    # if a:
    #     user=users.filter(email__iexact==a)
    #     serializer=UserSerializer(user,many=True)
    #     return Response(serializer.data)
    # else:
    serializer=MediaFileSerializer(users,many=True,context={'request': request})
    return Response(serializer.data)



@api_view(['POST']) #method type
def create_images(request):
        serializer= MediaFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "data created successfully", 'data': serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET']) #method type
def get_product(request):
    a = request.query_params.get('categoryname')
    product_id = request.query_params.get('id')
    users=products.objects.all()

    if a:
        users=users.filter(categorie__categories__iexact=a)
    if product_id:
        users = users.filter(id=product_id)

    serializer=productSerializer(users,many=True,context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def get_Userbyid(request,pk):
   product=products.objects.get(pk=pk)
   serializer=productSerializer(product,context={'request': request})
   return Response(serializer.data)


@api_view(['GET'])
def get_last_8_products(request):

    products_list = products.objects.all().order_by('-id')[:8]

    serializer = productSerializer(
        products_list,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view(['POST']) #method type
def create_product(request):
        serializer= ProductFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "data created successfully", 'data': serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
