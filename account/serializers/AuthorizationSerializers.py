from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

User=get_user_model()

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