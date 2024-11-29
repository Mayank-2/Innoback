from django.urls import path
from .views import AdminAuth, AdminAllProduct, SearchProduct, AdminCategory, UpcomingProductView,ProductImageView,ProductImageDetailView

urlpatterns = [
    path('api/admin/auth', AdminAuth.as_view(), name="adminAuth"),
    path('api/admin/allproduct', AdminAllProduct.as_view(), name="adminAllProduct"),
    path('api/admin/updateproduct/<str:product_id>',
         AdminAllProduct.as_view(), name="adminUpdateProduct"),
    path('api/admin/searchproduct/<str:query>',
         SearchProduct.as_view(), name="adminsearchProduct"),
    path('api/admin/product/delete/<str:id>',
         AdminAllProduct.as_view(), name="delete_product"),

    path('api/admin/allcategory', AdminCategory.as_view(), name="adminAllCategory"),
    path('api/admin/category/<str:id>',
         AdminCategory.as_view(), name="adminUpdateCategory"),
    path('api/admin/category/delete/<str:id>',
         AdminCategory.as_view(), name="delete_category"),

    path('api/upcoming-products', UpcomingProductView.as_view(),
         name='upcoming-product'),
    path('api/upcoming-products/<uuid:pk>',
         UpcomingProductView.as_view(), name='upcoming-product-next'),
    path('api/admin/product_images',
         ProductImageView.as_view(), name='product-image'),
    path('api/admin/product_image/<uuid:pk>',
         ProductImageDetailView.as_view(), name='productImage'),
     
]
