from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback_type', 'is_anonymous', 'full_name',
                   'contact_type', 'status', 'created_at')
    list_filter = ('feedback_type', 'status', 'is_anonymous', 'created_at')
    search_fields = ('full_name', 'message', 'contact_value')
    list_editable = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Информация об обращении', {
            'fields': ('feedback_type', 'is_anonymous', 'created_at')
        }),
        ('Контактные данные', {
            'fields': ('full_name', 'contact_type', 'contact_value'),
            'classes': ('collapse',)
        }),
        ('Содержание', {
            'fields': ('message',)
        }),
        ('Обработка', {
            'fields': ('status', 'admin_comment')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Делаем все поля обращения readonly кроме статуса и комментария"""
        if obj:  # редактирование
            return ['feedback_type', 'is_anonymous', 'full_name',
                   'contact_type', 'contact_value', 'message', 'created_at']
        return ['created_at']

