from rest_framework import serializers
from .models import User,AddCart
from image.serializer import productSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class AddtoCart(serializers.ModelSerializer):
    class Meta:
        model= AddCart
        fields='__all__'

class allProductSerializer(serializers.ModelSerializer):
    product=productSerializer(read_only=True)

    class Meta:
        model= AddCart
        fields=['user','product','quantity']