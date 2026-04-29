from django.shortcuts import render
from django.http import JsonResponse
import re

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User, AddCart
from .Serializer import UserSerializer, AddtoCart, allProductSerializer
from Shoe.image.models import products


@api_view(['GET'])
def get_users(request):
    search_name = request.query_params.get('name')
    users = User.objects.all()
    total_count = users.count()

    if search_name:
        users = users.filter(name__icontains=search_name)

    serializer = UserSerializer(users, many=True)
    return Response({"totalcount": total_count, "data": serializer.data})


@api_view(['POST'])
def create_user(request):
    name = (request.data.get('name') or "").strip()
    email = (request.data.get('email') or "").strip()
    password = request.data.get('password') or ""

    if not name:
        return Response({'message': "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not email:
        return Response({'message': "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not password:
        return Response({'message': "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'message': "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 8:
        return Response({'message': "Password must be at least 8 characters"}, status=status.HTTP_400_BAD_REQUEST)

    if not re.search(r'[A-Z]', password):
        return Response({'message': "Password must contain at least one uppercase letter"}, status=status.HTTP_400_BAD_REQUEST)

    if not re.search(r'[a-z]', password):
        return Response({'message': "Password must contain at least one lowercase letter"}, status=status.HTTP_400_BAD_REQUEST)

    if not re.search(r'\d', password):
        return Response({'message': "Password must contain at least one number"}, status=status.HTTP_400_BAD_REQUEST)

    if not re.search(r'[@$!%*?&]', password):
        return Response({'message': "Password must contain at least one special character"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()
    data['name'] = name
    data['email'] = email
    data['password'] = password

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    email = (request.data.get('email') or "").strip()
    password = request.data.get('password') or ""

    if not email:
        return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not password:
        return Response({'message': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()

    if not user:
        return Response({'message': 'No mail ID found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)

    if password == user.password:
        return Response({'message': 'SignIn Successful', 'data': serializer.data}, status=status.HTTP_200_OK)

    return Response({'message': 'Password invalid'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def add_to_cart(request):
    user_id = request.data.get("user")
    product_id = request.data.get("product")
    quantity = request.data.get("quantity", 1)

    if not user_id:
        return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantity = int(quantity)
    except ValueError:
        return Response({"error": "Quantity must be a number"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        product = products.objects.get(id=product_id)
    except products.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    cart_item, created = AddCart.objects.get_or_create(
        user=user,
        product=product,
        defaults={"quantity": quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response({"message": "Added to cart"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getcart_users(request):
    users = AddCart.objects.all()
    total_count = users.count()
    serializer = AddtoCart(users, many=True)

    return Response({"totalcount": total_count, "data": serializer.data})


@api_view(['GET'])
def getcart_Userbyid(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    cart_items = AddCart.objects.filter(user=user)

    if not cart_items.exists():
        return Response({"error": "Cart is empty", "data": []}, status=status.HTTP_404_NOT_FOUND)

    serializer = allProductSerializer(
        cart_items,
        many=True,
        context={'request': request}
    )

    return Response({
        "message": "Cart fetched successfully",
        "data": serializer.data
    }, status=status.HTTP_200_OK)