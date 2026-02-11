from django.contrib import admin
from .models import OnboardingDay, OnboardingMedia, DailyReport


class OnboardingMediaInline(admin.TabularInline):
    """Inline для медиа-материалов в дне онбординга"""
    model = OnboardingMedia
    extra = 1
    fields = ('media_type', 'title', 'link', 'file', 'order')
    ordering = ('order',)


@admin.register(OnboardingDay)
class OnboardingDayAdmin(admin.ModelAdmin):
    list_display = ('day_number', 'title', 'deadline_time', 'is_active', 'order', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'instructions')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'day_number')
    inlines = [OnboardingMediaInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('day_number', 'title', 'description')
        }),
        ('Инструкции и дедлайн', {
            'fields': ('instructions', 'deadline_time')
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # При редактировании
            return ['created_at', 'updated_at']
        return []


@admin.register(OnboardingMedia)
class OnboardingMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'onboarding_day', 'media_type', 'order', 'created_at')
    list_filter = ('media_type', 'onboarding_day')
    search_fields = ('title', 'onboarding_day__title')
    list_editable = ('order',)
    ordering = ('onboarding_day__day_number', 'order')

    fieldsets = (
        ('Привязка', {
            'fields': ('onboarding_day',)
        }),
        ('Содержимое', {
            'fields': ('media_type', 'title', 'link', 'file')
        }),
        ('Настройки', {
            'fields': ('order',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Подсказки в зависимости от типа
        form.base_fields['link'].help_text = 'Для типов: Ссылка, Видео (URL YouTube/Vimeo)'
        form.base_fields['file'].help_text = 'Для типов: Изображение, Файл'
        return form


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'intern_display', 'day_display',
        'status', 'submitted_at', 'reviewer_display', 'reviewed_at'
    )
    list_filter = ('status', 'submitted_at', 'reviewed_at', 'onboarding_day')
    search_fields = ('intern__email', 'intern__first_name', 'intern__last_name', 'what_done', 'problems')
    readonly_fields = ('created_at', 'submitted_at', 'reviewed_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Информация', {
            'fields': ('intern', 'onboarding_day', 'status', 'created_at')
        }),
        ('Содержание отчёта', {
            'fields': ('what_done', 'what_will_do', 'problems', 'attachment_link', 'attachment_file')
        }),
        ('Отправка', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
        ('Проверка', {
            'fields': ('reviewer', 'reviewer_comment', 'reviewed_at'),
            'classes': ('collapse',)
        }),
    )

    def intern_display(self, obj):
        name = f"{obj.intern.first_name} {obj.intern.last_name}".strip()
        return name or obj.intern.email
    intern_display.short_description = 'Стажёр'

    def day_display(self, obj):
        return f"День {obj.onboarding_day.day_number}"
    day_display.short_description = 'День'

    def reviewer_display(self, obj):
        if obj.reviewer:
            name = f"{obj.reviewer.first_name} {obj.reviewer.last_name}".strip()
            return name or obj.reviewer.email
        return '-'
    reviewer_display.short_description = 'Проверяющий'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != 'draft':
            # Если не черновик, делаем поля отчёта readonly
            return [
                'intern', 'onboarding_day',
                'what_done', 'what_will_do', 'problems',
                'attachment_link', 'attachment_file',
                'created_at', 'submitted_at', 'reviewed_at'
            ]
        return ['created_at', 'submitted_at', 'reviewed_at']

    def has_delete_permission(self, request, obj=None):
        # Удалять могут только суперадмины
        return request.user.is_superuser

