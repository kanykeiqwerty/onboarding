from rest_framework import serializers
from .models import Regulation


class RegulationSerializer(serializers.ModelSerializer):
    """Сериализатор для регламентов"""
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)

    class Meta:
        model = Regulation
        fields = ['id', 'title', 'description', 'content_type', 'content_type_display',
                 'link', 'file', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

