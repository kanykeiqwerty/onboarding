from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from account.models import DepartmentEnum
from account.utils import send_intern_credentials_email
from onboard import settings

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
        plain_password = validated_data['password']
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=False,  
            is_superuser=False
        )

        login_url = getattr(settings, 'FRONTEND_LOGIN_URL', 'http://localhost:8000/api/v1/account/login')
        send_intern_credentials_email(
            user_email=user.email,
            password=plain_password,
            login_url=login_url
        )
        return user   
    
class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения информации о пользователе
    """
    role = serializers.SerializerMethodField()
    # department = serializers.ChoiceField(choices=[(dep.name, dep.value) for dep in DepartmentEnum])
    # position = serializers.ChoiceField(choices=[], required=False)
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',  'is_active', 'role', 'date_joined')
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


class UserSelfSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'date_joined',
            'profile_photo',
            'phone',
            'telegram',
            'linkedin',
            'github',
        )
        read_only_fields = ('id', 'email', 'role', 'date_joined')

    def get_role(self, obj):
        if obj.is_superuser:
            return 'superadmin'
        elif obj.is_staff:
            return 'admin'
        return 'intern'
    
    def validate_profile_photo(self, value):
        """Валидация размера и формата фото"""
        if value:
            # Проверка размера (например, максимум 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Размер файла не должен превышать 5MB")
            
            # Проверка формата
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            ext = value.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    f"Неподдерживаемый формат. Используйте: {', '.join(valid_extensions)}"
                )
        return value