from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """Сериализатор для создания обратной связи"""

    class Meta:
        model = Feedback
        fields = ['id', 'feedback_type', 'is_anonymous', 'full_name',
                 'contact_type', 'contact_value', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """Валидация: если не анонимно, требуются контакты"""
        if not data.get('is_anonymous'):
            if not data.get('full_name'):
                raise serializers.ValidationError({'full_name': 'Обязательное поле для неанонимной формы'})
            if not data.get('contact_type') or not data.get('contact_value'):
                raise serializers.ValidationError({'contact_value': 'Укажите контакт для связи'})
        return data


class FeedbackAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для админ-панели (просмотр и управление)"""
    feedback_type_display = serializers.CharField(source='get_feedback_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

