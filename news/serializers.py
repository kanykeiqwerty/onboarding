from rest_framework import serializers
from .models import News, Employee, WelcomeBlock


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для новостей"""

    class Meta:
        model = News
        fields = ['id', 'title', 'short_description', 'full_text', 'image',
                 'published_date', 'is_active', 'order']
        read_only_fields = ['id', 'published_date']


class NewsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка новостей (слайдер)"""

    class Meta:
        model = News
        fields = ['id', 'title', 'short_description', 'image', 'published_date']
        read_only_fields = ['id', 'published_date']


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для сотрудников"""

    class Meta:
        model = Employee
        fields = ['id', 'photo', 'full_name', 'position', 'department',
                 'contact', 'order', 'is_active']
        read_only_fields = ['id']


class WelcomeBlockSerializer(serializers.ModelSerializer):
    """Сериализатор для приветственного блока"""

    class Meta:
        model = WelcomeBlock
        fields = ['id', 'title', 'text', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

