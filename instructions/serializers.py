from rest_framework import serializers
from .models import Instruction


class InstructionSerializer(serializers.ModelSerializer):
    """Сериализатор для инструкций"""
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)

    class Meta:
        model = Instruction
        fields = ['id', 'title', 'content_type', 'content_type_display',
                 'text_content', 'link', 'file', 'is_active',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

