from django.contrib import admin
from .models import UpcomingProduct,Category,Products,ProductImage,Orders,Order_items
# Register your models here.

@admin.register(UpcomingProduct)
class AdminUpcomingProduct(admin.ModelAdmin):
    list_display = ('id', 'title','date')

@admin.register(Category)
class AdminCategory (admin.ModelAdmin):
    list_display = ('id', 'category')

@admin.register(Products)
class AdminProducts(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(ProductImage)
class AdminProductImage(admin.ModelAdmin):
    list_display = ('id',"product")

@admin.register(Orders)
class AdminOrders(admin.ModelAdmin):
    list_display = ('id', 'customer')

@admin.register(Order_items)
class AdminOrder_items(admin.ModelAdmin):
    list_display = ('id', 'order', 'product')
