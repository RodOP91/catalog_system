from functools import wraps

from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status

from .models import AuthToken

def require_token(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token_value = request.META.get('HTTP_AUTHORIZATION', '').replace('Token ', '')
        
        if not token_value:
            return Response({'info': 'Acceso denegado. Token no proporcionado.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = AuthToken.objects.get(token=token_value)
        except AuthToken.DoesNotExist:
            token = None
            
        if token.is_expired():
            return Response({'info': 'Acceso denegado. Token expirado.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if token and isinstance(token, AuthToken) and not token.is_expired():
            return view_func(request, *args, **kwargs)
        else:
            return Response({'info': 'Acceso denegado. Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper
