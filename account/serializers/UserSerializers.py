from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

User=get_user_model()

class InternCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания стажеров (админы и суперадмин)
    """
    password = serializers.CharField(min_length=6, max_length=100, required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=False,  
            is_superuser=False
        )
        return user   
    
class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения информации о пользователе
    """
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'role', 'date_joined')
        read_only_fields = ('id', 'date_joined')
    
    def get_role(self, obj):
        if obj.is_superuser:
            return 'superadmin'
        elif obj.is_staff:
            return 'admin'
        else:
            return 'intern'
        

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления пользователя
    """
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_active')