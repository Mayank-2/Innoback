from rest_framework import serializers
from accounts.models import User
from products.models import Products,Category,UpcomingProduct,ProductImage

class User_Login_serializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class AllProductsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class UpcomingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingProduct
        fields = ['id', 'poster', 'date', 'title']

