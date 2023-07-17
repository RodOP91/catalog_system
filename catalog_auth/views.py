import secrets

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from .models import *
from .serializers import *
from .decorators import *

### USER CRUDL ###

class UserCreateListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @method_decorator(require_token)
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    @method_decorator(require_token)
    def post(self, request):
        data = request.data.copy()
        data["password"] = make_password(data["password"])
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except Exception as e:
                print(f"Ocurrió un error al crear el Usuario: {e}")
            try:
                token = AuthToken.objects.create(user=user)
            except Exception as e:
                print(f"Ocurrió un error al crear el Token: {e}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @method_decorator(require_token)
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "No se encontró al usuario."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @method_decorator(require_token)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

    @method_decorator(require_token)
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"info": "Usuario eliminado con éxito."},status=status.HTTP_204_NO_CONTENT)


### AUTH ###

class TokenAuthenticationView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        
        if user:
            token = AuthToken.objects.create(user=user)
            token_serializer = AuthTokenSerializer(token)
            response_data = token_serializer.data
            response_data['info'] = 'Token generado con éxito.'
            return Response(response_data)

        else:
            return Response({'detail': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
