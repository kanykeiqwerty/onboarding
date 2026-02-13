from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

User=get_user_model()

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
    

class SuperAdminUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)
    role_update = serializers.ChoiceField(
        choices=['superadmin', 'admin', 'intern'],
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'role',
            'role_update',
            'date_joined',
        )
        read_only_fields = ('id', 'email', 'date_joined')

    def get_role(self, obj):
        if obj.is_superuser:
            return 'superadmin'
        elif obj.is_staff:
            return 'admin'
        return 'intern'

    def update(self, instance, validated_data):
        role = validated_data.pop('role_update', None)
        request = self.context.get('request')

        # обычные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # смена роли — только суперадмин
        if role is not None:
            if not request or not request.user.is_superuser:
                raise serializers.ValidationError(
                    {'role': 'Only superadmin can change roles.'}
                )

            # защита от самострела
            if instance == request.user:
                raise serializers.ValidationError(
                    {'role': 'You cannot change your own role.'}
                )

            # защита последнего суперадмина
            if (
                instance.is_superuser
                and role != 'superadmin'
                and User.objects.filter(is_superuser=True).count() == 1
            ):
                raise serializers.ValidationError(
                    {'role': 'You cannot remove the last superadmin.'}
                )

            if role == 'superadmin':
                instance.is_superuser = True
                instance.is_staff = True
            elif role == 'admin':
                instance.is_superuser = False
                instance.is_staff = True
            else:
                instance.is_superuser = False
                instance.is_staff = False

        instance.save()
        return instance