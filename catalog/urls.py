from django.urls import path
from .views import *

urlpatterns = [
    path('product/', CreateProductAPIView.as_view(), name='create-product'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<str:sku>/', ProductDetailAPIView.as_view(), name='product-detail'),
]
