from rest_framework import serializers
from .models import News, Employee, WelcomeBlock


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для новостей"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'short_description', 'full_text', 'image',
                 'image_url', 'published_date', 'is_active', 'order']
        read_only_fields = ['id', 'published_date']

    def get_image_url(self, obj):
        """Возвращает полный URL изображения"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class NewsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка новостей (слайдер)"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'short_description', 'image', 'image_url', 'published_date']
        read_only_fields = ['id', 'published_date']

    def get_image_url(self, obj):
        """Возвращает полный URL изображения"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для сотрудников"""
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'photo', 'photo_url', 'full_name', 'position', 'department',
                 'contact', 'order', 'is_active']
        read_only_fields = ['id']

    def get_photo_url(self, obj):
        """Возвращает полный URL фотографии"""
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class WelcomeBlockSerializer(serializers.ModelSerializer):
    """Сериализатор для приветственного блока"""

    class Meta:
        model = WelcomeBlock
        fields = ['id', 'title', 'text', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

