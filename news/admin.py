from django.contrib import admin
from .models import News, Employee, WelcomeBlock


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'published_date', 'is_active', 'order')
    list_filter = ('is_active', 'published_date')
    search_fields = ('title', 'short_description', 'full_text')
    list_editable = ('is_active', 'order')
    ordering = ('order', '-published_date')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'short_description', 'full_text', 'image')
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'contact', 'is_active', 'order')
    list_filter = ('is_active', 'department', 'position')
    search_fields = ('full_name', 'position', 'department')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'full_name')

    fieldsets = (
        ('Информация о сотруднике', {
            'fields': ('photo', 'full_name', 'position', 'department', 'contact')
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(WelcomeBlock)
class WelcomeBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'text')
    list_editable = ('is_active',)

    fieldsets = (
        ('Содержание', {
            'fields': ('title', 'text')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )

