from django.contrib import admin
from django import forms
from .models import WorkScheduleType, UserSchedule, Holiday, WeekDay


# --- Форма для WorkScheduleType с чекбоксами ---
class WorkScheduleTypeForm(forms.ModelForm):
    work_days = forms.MultipleChoiceField(
        choices=WeekDay.choices,
        widget=forms.CheckboxSelectMultiple,
        label='Рабочие дни',
        required=True,
    )

    class Meta:
        model = WorkScheduleType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.work_days:
            self.initial['work_days'] = self.instance.work_days

    def clean_work_days(self):
        return list(map(int, self.cleaned_data['work_days']))


# --- Inline для пользователей графика ---
class UserScheduleInline(admin.TabularInline):
    model = UserSchedule
    fields = ('user_display', 'created_at')
    readonly_fields = ('user_display', 'created_at')
    extra = 0
    can_delete = False

    def user_display(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name or obj.user.email
    user_display.short_description = 'Пользователь'


# --- Админка для WorkScheduleType ---
@admin.register(WorkScheduleType)
class WorkScheduleTypeAdmin(admin.ModelAdmin):
    form = WorkScheduleTypeForm
    list_display = ('name', 'start_time', 'end_time', 'is_default', 'is_active')
    list_filter = ('is_default', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_default', 'is_active')
    inlines = [UserScheduleInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description')
        }),
        ('Рабочие дни', {
            'fields': ('work_days',),
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


# --- Админка для UserSchedule ---
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


# --- Админка для Holiday ---
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
