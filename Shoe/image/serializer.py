from rest_framework import serializers
from .models import img, products

class MediaFileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = img
        fields = ['id', 'categories', 'image']  

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    

class ProductFileSerializer(serializers.ModelSerializer):

    productimage = serializers.SerializerMethodField()

    class Meta:
        model = products
        fields = '__all__'

    def get_productimage(self, obj):
        request = self.context.get('request')   
        if obj.productimage:
            return request.build_absolute_uri(obj.productimage.url)
        return None
    
class productSerializer(serializers.ModelSerializer):
        categorie=MediaFileSerializer(read_only=True)
        class Meta:
            model = products
            fields = ['id', 'productimage','productname','currentprice','previousprice','descripe','count','categorie']


