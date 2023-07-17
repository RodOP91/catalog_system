from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = '__all__'

class AuthTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='get_token', read_only=True)
    
    class Meta:
        model = AuthToken
        fields = ('token', 'expires_at')
