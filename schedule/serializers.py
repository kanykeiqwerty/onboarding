from rest_framework import serializers
from .models import WorkScheduleType, UserSchedule, Holiday, WeekDay
from django.contrib.auth import get_user_model

User = get_user_model()


class WorkScheduleTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для типов графиков работы"""
    work_days = serializers.ListField(
        child=serializers.ChoiceField(choices=WeekDay.choices)
    )
    users = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WorkScheduleType
        fields = [
            'id', 'name', 'description', 'work_days', 'start_time', 'end_time',
            'lunch_start', 'lunch_end', 'breaks', 'is_default', 'is_active', 'users'
        ]
        read_only_fields = ['id', 'users']

    def get_users(self, obj):
        return [{'id': u.user.id, 'email': u.user.email} for u in obj.users.all()]


class UserScheduleSerializer(serializers.ModelSerializer):
    """Сериализатор для графика пользователя"""
    schedule_details = WorkScheduleTypeSerializer(source='schedule_type', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserSchedule
        fields = ['id', 'user', 'user_email', 'schedule_type', 'schedule_details',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MyScheduleSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра/обновления своего графика"""
    schedule_details = WorkScheduleTypeSerializer(source='schedule_type', read_only=True)

    class Meta:
        model = UserSchedule
        fields = ['id', 'schedule_type', 'schedule_details', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class HolidaySerializer(serializers.ModelSerializer):
    """Сериализатор для праздников"""

    class Meta:
        model = Holiday
        fields = ['id', 'date', 'name', 'is_working_day', 'created_at']
        read_only_fields = ['id', 'created_at']
