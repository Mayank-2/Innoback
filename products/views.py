
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UpcomingProduct, Category, Products, ProductImage, Orders, Order_items
from .serializers import AllUpcomingProductSerializer, AllCategorySerializer, AllProductsSerializer, AllProductsImagesSerializer, AllOrdersSerializer, Order_ItemsSerializer, PlaceOrderDataSerializer
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from accounts.authentication import CustomAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
today = timezone.now()
# Create your views here.


class AllUpcomingProductView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            upcoming_products = UpcomingProduct.objects.filter(date__gt=today)
            serializer = AllUpcomingProductSerializer(
                upcoming_products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AllCategoryView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = AllCategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AllProductsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            products = Products.objects.all()
            serializer = AllProductsSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        






class CategoricalProductView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def get(self, request, category):
        try:
            products = Products.objects.filter(category__category=category)
            serializer = AllProductsSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class MainProductView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def get(self, request, id):
        try:
            product = Products.objects.get(id=id)
            product_serializer = AllProductsSerializer(product)
            product_images = ProductImage.objects.filter(
                product=product).select_related("product")
            image_serializer = AllProductsImagesSerializer(
                product_images, many=True)
            return Response({"product": product_serializer.data, "images": image_serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class AllOrdersView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            orders = Orders.objects.filter(
                customer=user).select_related("customer").order_by('-created_at')

            orders_serializer = AllOrdersSerializer(orders, many=True)
            return Response(orders_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class OrderItemsView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Orders.objects.get(id=order_id)
            order_items = Order_items.objects.filter(
                order=order).select_related("order")
            serializer = Order_ItemsSerializer(order_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class PlaceOrderView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PlaceOrderDataSerializer(data=request.data)
        if serializer.is_valid():
            total_sum = serializer.validated_data.get("total_amount")
            products = serializer.validated_data.get('products')

            try:
                with transaction.atomic():
                    # Create the order
                    order = Orders.objects.create(
                        customer=user, total_amount=total_sum, status="confirmed")

                    # Create the order items
                    for item in products:
                        product_id = item["id"]
                        quantity = item["quantity"]
                        # Validate product existence
                        product = Products.objects.get(id=product_id)
                        # Create the order item
                        Order_items.objects.create(
                            order=order, product=product, quantity=quantity)

                    return Response({"message": "Order placed successfully!", "order_id": order.id}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CancelOrderView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, order_id):
        try:
            order = Orders.objects.get(id=order_id)
            order.status = "cancelled"
            order.save()
            return Response({"message": "Order cancelled successfully!"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
