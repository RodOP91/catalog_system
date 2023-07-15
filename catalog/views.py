from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
class ProductDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'sku'
    def get(self, request, sku):
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            return Response(
                {"error": "No se encontró el producto."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
class CreateProductAPIView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class UpdateProductAPIView(APIView):
#    def 
"""
Product List: /api/products/ (GET)
Product Detail: /api/products/{sku}/ (GET)
Create Product: /api/products/ (POST)
Update Product: /api/products/{sku}/ (PUT/PATCH)
Delete Product: /api/products/{sku}/ (DELETE)
User List: /api/users/ (GET) [Only accessible by admins]
User Detail: /api/users/{user_id}/ (GET) [Only accessible by admins]
Create User: /api/users/ (POST) [Only accessible by admins]
Update User: /api/users/{user_id}/ (PUT/PATCH) [Only accessible by admins]
Delete User: /api/users/{user_id}/ (DELETE) [Only accessible by admins]
"""