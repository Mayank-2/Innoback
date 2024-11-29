from django.urls import path
from .views import AllUpcomingProductView,AllCategoryView,AllProductsView,CategoricalProductView,MainProductView,AllOrdersView,OrderItemsView,PlaceOrderView,CancelOrderView
urlpatterns = [
    path('AllUpcomingProduct/',AllUpcomingProductView.as_view(),name="AllUpcomingProduct"),
    path('allCategory/',AllCategoryView.as_view(),name="allcategory"),
    path('category/<str:category>',CategoricalProductView.as_view(),name="categoryProducts"),
    path('allproducts/',AllProductsView.as_view(),name="allProducts"),
    path('product/<str:id>',MainProductView.as_view(),name="mainProducts"),
    path('orders/',AllOrdersView.as_view(),name="Orders"),
    path('order_items/<str:order_id>',OrderItemsView.as_view(),name="order_items"),
    path('order/placeorder',PlaceOrderView.as_view(),name="place_order"),
    path('order/cancel/<str:order_id>',CancelOrderView.as_view(),name="cancel_order")

]
