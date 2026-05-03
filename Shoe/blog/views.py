from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,AddCart
from .Serializer import UserSerializer,AddtoCart,allProductSerializer
from Shoe.image.models import products

# from database

@api_view(['GET']) #method type
def get_users(request):
    a=request.query_params.get('name')
    users=User.objects.all()
    d=len(users)
    if a:
        users=User.objects.filter(name__icontains=a)
    serializer=UserSerializer(users,many=True)
    return Response({"totalcount":d,'data':serializer.data})


@api_view(['POST'])
def create_user(request):
    name = (request.data.get('name') or "").strip()
    email = (request.data.get('email') or "").strip()
    password = request.data.get('password') or ""

    # Name validation
    if not name:
        return Response({'message': "Name is required"},status=status.HTTP_400_BAD_REQUEST)

    # Email validation
    elif not email:
        return Response(
            {'message': "Email is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif User.objects.filter(email=email).exists():
        return Response(
            {'message': "Mail already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Password validation
    elif not password:
        return Response(
            {'message': "Password is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif len(password) < 8:
        return Response(
            {'message': "Password must be at least 8 characters"},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif not re.search(r'[A-Z]', password):
        return Response(
            {'message': "Password must contain at least one uppercase letter"},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif not re.search(r'[a-z]', password):
        return Response(
            {'message': "Password must contain at least one lowercase letter"},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif not re.search(r'\d', password):
        return Response(
            {'message': "Password must contain at least one number"},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif not re.search(r'[@$!%*?&]', password):
        return Response(
            {'message': "Password must contain at least one special character"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Save user
    data = {
    "name": name,
    "email": email,
    "password": password,
    }

    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['post'])
def login_user(request):
    email=request.data.get('email')
    password=request.data.get('password')

    if email.strip=='':
        return Response({'message': 'Email is required'},status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        d=User.objects.filter(email=email).first()
        serializer=UserSerializer(d)
        if password==d.password:   
         return Response({'message':'SingIn Successful','data': serializer.data},status=status.HTTP_200_OK)
        elif password!=d.password:
            return Response({'message':'password invalid'},status=status.HTTP_401_UNAUTHORIZED)
    else:
         return Response({'message': 'No mail ID found'}, status=status.HTTP_404_NOT_FOUND)
    
# @csrf_exempt
@api_view(['POST'])
def add_to_cart(request):
    user_id = request.data.get("user")
    product_id = request.data.get("product")
    quantity = int(request.data.get("quantity", 1))

    if not user_id:
        return Response({"error": "User ID is required"}, status=400)

    if not product_id:
        return Response({"error": "Product ID is required"}, status=400)
    
    try:
        quantity = int(quantity)
    except:
        return Response({"error": "Quantity must be number"}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    try:
        product = products.objects.get(id=product_id)
    except products.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    cart_item, created = AddCart.objects.get_or_create(
        user=user,
        product=product,
        defaults={"quantity": quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response({"message": "Added to cart"})

@api_view(['GET']) #method type
def getcart_users(request):
    a=request.query_params.get('name')
    users=AddCart.objects.all()
    d=len(users)   
    serializer=AddtoCart(users,many=True)
    return Response({"totalcount":d,'data':serializer.data})


@api_view(['DELETE'])
def delete_cart(request, pk):
    try:
        cart_item = allProductSerializer.objects.get(id=pk)
        cart_item.delete()
        return Response({"message": "Cart item deleted"}, status=200)
    except allProductSerializer.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=404)


@api_view(['GET'])
def getcart_Userbyid(request, id):

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found","data":[]}, status=404)

    cart_items = AddCart.objects.filter(user=user)

    if not cart_items.exists():
        return Response({"error": "Cart is empty",'data':[]}, status=404)

    serializer = allProductSerializer(cart_items, many=True,context={'request': request})

    return Response({
        "message": "Cart fetched successfully",
        "data": serializer.data
    }, status=200)


