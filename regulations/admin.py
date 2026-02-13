from django.contrib import admin
from .models import Regulation


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'is_active', 'order', 'updated_at')
    list_filter = ('content_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'title')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description')
        }),
        ('Контент', {
            'fields': ('content_type', 'link', 'file')
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['link'].help_text = 'Для типа "Ссылка"'
        form.base_fields['file'].help_text = 'Для типа "Файл"'
        return form

