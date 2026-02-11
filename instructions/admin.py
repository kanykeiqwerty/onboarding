from django.contrib import admin
from .models import Instruction


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'is_active', 'updated_at')
    list_filter = ('content_type', 'is_active', 'created_at')
    search_fields = ('title', 'text_content')
    list_editable = ('is_active',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content_type')
        }),
        ('Контент', {
            'fields': ('text_content', 'link', 'file'),
            'description': 'Заполните одно из полей в зависимости от типа контента'
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['text_content'].help_text = 'Для типа "Текст"'
        form.base_fields['link'].help_text = 'Для типа "Ссылка"'
        form.base_fields['file'].help_text = 'Для типа "Файл"'
        return form

