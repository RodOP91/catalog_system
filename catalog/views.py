from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework import status, generics

from .models import *
from .serializers import *
from catalog_auth.decorators import *
from catalog_auth.models import User

### PRODUCT CRUDL ###

"""
ProductCreateListAPIView takes care of:
    POST
    GET(all)
"""
class ProductCreateListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get(self, request):
        users = Product.objects.all()
        serializer = ProductSerializer(users, many=True)
        return Response(serializer.data)
    
    @method_decorator(require_token)
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
ProductDetailUpdateDeleteAPIView takes care of:
    GET (by sku)
    PATCH
    PUT
    DELETE
"""
class ProductDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'sku'

    def get(self, request, sku):
        print_request_data(request)
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            return Response(
                {"error": "No se encontró el producto."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)

        #user = request.user
        if not request.headers.get('Authorization'):
            product.query_count += 1
            product.save()
        return Response(serializer.data)
    
    @method_decorator(require_token)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @method_decorator(require_token)
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def print_request_data(request):
    print("Request method:", request.method)
    print("Request path:", request.path)
    print("Request query parameters:", request.query_params)
    print("Request headers:", request.headers)
    print("Request body:", request.data)
    
    # You can access other attributes as needed
    
    return Response("Data printed in the console.")