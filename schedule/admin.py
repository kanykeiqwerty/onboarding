from django.contrib import admin
from .models import WorkScheduleType, UserSchedule, Holiday


@admin.register(WorkScheduleType)
class WorkScheduleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'is_default', 'is_active')
    list_filter = ('is_default', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_default', 'is_active')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description')
        }),
        ('Рабочие дни', {
            'fields': ('work_days',),
            'description': 'Список номеров дней недели (1=Пн, 2=Вт, ..., 7=Вс). Например: [1,2,3,4,5] для Пн-Пт'
        }),
        ('Время работы', {
            'fields': ('start_time', 'end_time', 'lunch_start', 'lunch_end')
        }),
        ('Дополнительные перерывы', {
            'fields': ('breaks',),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('is_default', 'is_active')
        }),
    )


@admin.register(UserSchedule)
class UserScheduleAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'schedule_type', 'created_at', 'updated_at')
    list_filter = ('schedule_type', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    autocomplete_fields = ['user']

    def user_display(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name or obj.user.email
    user_display.short_description = 'Пользователь'


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'is_working_day')
    list_filter = ('is_working_day', 'date')
    search_fields = ('name',)
    date_hierarchy = 'date'
    list_editable = ('is_working_day',)

    fieldsets = (
        ('Информация о празднике', {
            'fields': ('date', 'name', 'is_working_day')
        }),
    )

