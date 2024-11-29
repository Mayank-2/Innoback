from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from django.middleware import csrf
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from accounts.renderers import UserRenderer
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from accounts.models import User, Profile
from .customAdminAuth import CustomAdminAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.conf import settings
from .customThrottle import CustomAnonRateThrottle
from .serializers import User_Login_serializer, ProductSerializer, CategorySerializer, UpcomingProductSerializer,AllProductsImagesSerializer
from products.models import Products, Category, UpcomingProduct,ProductImage
today = timezone.now().date()
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class AdminAuth(APIView):
    renderer_classes = [UserRenderer]
    throttle_classes = [CustomAnonRateThrottle]
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = User_Login_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            if not email or not password:
                return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(email=email, password=password)

            if user and user.is_admin:
                token = get_tokens_for_user(user)
                response = Response(
                    {"data": "Authentication successful", "user": user.name}, status=status.HTTP_200_OK)
                response.set_cookie(key=settings.SIMPLE_JWT['Admin_AUTH_COOKIES'],
                                    value=token["access"],
                                    domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                                    path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
                                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    secure=False,
                                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                    )
                response.set_cookie(key=settings.SIMPLE_JWT['Admin_COOKIE_REFRESH'],
                                    value=token["refresh"],
                                    domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
                                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                    )

                csrf.get_token(request)
                return response
            else:
                return Response({"error": "Authentication Failed"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UpcomingProductView(APIView):

    def get(self, request):
        try:
            upcoming_product = UpcomingProduct.objects.all()
            serializer = UpcomingProductSerializer(upcoming_product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = UpcomingProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        try:
            upcoming_product = UpcomingProduct.objects.get(pk=pk)
            serializer = UpcomingProductSerializer(upcoming_product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            upcoming_product = UpcomingProduct.objects.get(pk=pk)
            upcoming_product.delete()
            return Response({"message": "Upcoming Product deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminCategory(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [CustomAdminAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "Category created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "Category updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        category = Category.objects.get(id=id)
        category.delete()
        return Response({"data": "Category deleted successfully"}, status=status.HTTP_200_OK)


class AdminAllProduct(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [CustomAdminAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "Product created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = Products.objects.get(id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": "Product updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = Products.objects.get(id=id)
        product.delete()
        return Response({"data": "Product deleted successfully"}, status=status.HTTP_200_OK)
    
class ProductImageView(APIView):
    authentication_classes = [CustomAdminAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AllProductsImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductImageDetailView(APIView):
    
    authentication_classes = [CustomAdminAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            images = ProductImage.objects.filter(product=pk)
            serializer = AllProductsImagesSerializer(images,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductImage.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            image = ProductImage.objects.get(pk=pk)
            serializer = AllProductsImagesSerializer(image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ProductImage.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            image = ProductImage.objects.get(pk=pk)
            image.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ProductImage.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


class SearchProduct(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [CustomAdminAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, query):
        try:
            products = Products.objects.filter(name__icontains=query)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
