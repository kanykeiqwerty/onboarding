from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback_type', 'message_preview', 'is_anonymous',
                   'full_name', 'contact_display', 'status', 'created_at')
    list_filter = ('feedback_type', 'status', 'is_anonymous', 'created_at')
    search_fields = ('full_name', 'message', 'contact_value')
    list_editable = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def message_preview(self, obj):
        """Показывает первые 50 символов сообщения"""
        if len(obj.message) > 50:
            return obj.message[:50] + '...'
        return obj.message
    message_preview.short_description = 'Сообщение'

    def contact_display(self, obj):
        """Показывает тип контакта и сам контакт"""
        if obj.contact_type and obj.contact_value:
            return f"{obj.get_contact_type_display()}: {obj.contact_value}"
        elif obj.contact_type:
            return obj.get_contact_type_display()
        return '-'
    contact_display.short_description = 'Контакт'

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

