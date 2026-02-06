from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(min_length=6, max_length=100, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')
    
    
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AdminCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания админов (только суперадмин)
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
            is_staff=True,  
            is_superuser=False
        )
        return user
    
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


class LoginSerializer(TokenObtainPairSerializer):
    email=serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        user = authenticate(email=email, password=password)
        
        if user is None:
            raise serializers.ValidationError('Invalid email or password!')  # ✅ не раскрывать детали
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled!')
        
        refresh = self.get_token(user)

        if user.is_superuser:
            role = 'superadmin'
        elif user.is_staff:
            role = 'admin'
        else:
            role = 'intern'
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {  # ✅ добавить информацию о пользователе
                'id': user.id,
                'email': user.email,
                'role': role,
                'first_name':user.first_name,
                'last_name': user.last_name,
                
            }
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': _('Token is invalid or expired!')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=100, required=True)


# class RestorePasswordSerializer(serializers.Serializer):
#     code = serializers.CharField(max_length=100, required=True)
#     password = serializers.CharField(min_length=6, required=True)
#     password2 = serializers.CharField(min_length=6, required=True)

#     def validate(self, attrs):
#         password2 = attrs.pop('password2')
#         if password2 != attrs['password']:
#             raise serializers.ValidationError('Passwords didn\'t match!')
#         try:
#             user = User.objects.get(activation_code=attrs['code'])
#         except User.DoesNotExist:
#             serializers.ValidationError('Your code is incorrect!')
#         attrs['user'] = user
#         return attrs
        
#     def save(self, **kwargs):
#         data = self.validated_data
#         user = data['user']
#         user.set_password(data['password'])
#         user.activation_code = ''
#         user.save()
#         return user

# class SpamViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Contact
#         fields='__all__'
