from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^product/?$', ProductCreateListAPIView.as_view(), name='product-create-getall'),
    re_path(r'^product/(?P<sku>[\w-]+)/?$', ProductDetailUpdateDeleteAPIView.as_view(), name='product-detail-update-delete'),
]

