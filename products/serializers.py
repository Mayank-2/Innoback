from rest_framework import serializers
from .models import UpcomingProduct,Category,Products, ProductImage , Orders , Order_items


class AllUpcomingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingProduct
        fields = "__all__"
        
class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class AllProductsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.category
    class Meta:
        model = Products
        fields = '__all__'

class AllProductsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class AllOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class Order_ItemsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    
    def get_product(self, obj):
        return obj.product.name
    class Meta:
        model = Order_items
        fields = '__all__'


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField()

class PlaceOrderDataSerializer(serializers.Serializer):

    total_amount = serializers.IntegerField()
    products = serializers.ListField(
        child=ProductSerializer()   # Ensures the array contains integers
    )