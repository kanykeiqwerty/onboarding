from django.db import models
from onboard import settings
from django.utils.translation import gettext_lazy as _
import json


class WeekDay(models.IntegerChoices):
    MONDAY = 1, _('Понедельник')
    TUESDAY = 2, _('Вторник')
    WEDNESDAY = 3, _('Среда')
    THURSDAY = 4, _('Четверг')
    FRIDAY = 5, _('Пятница')
    SATURDAY = 6, _('Суббота')
    SUNDAY = 7, _('Воскресенье')



class WorkScheduleType(models.Model):
    """Типовой график работы"""
    name = models.CharField(_('Название'), max_length=100, help_text='Например: График 5/2')
    description = models.TextField(_('Описание'), blank=True)
    work_days = models.JSONField(
        _('Рабочие дни'),
        default=list,
        help_text='Список номеров рабочих дней недели: [1,2,3,4,5] для Пн-Пт'
    )
    start_time = models.TimeField(_('Начало рабочего дня'))
    end_time = models.TimeField(_('Окончание рабочего дня'))
    lunch_start = models.TimeField(_('Начало обеда'), blank=True, null=True)
    lunch_end = models.TimeField(_('Окончание обеда'), blank=True, null=True)
    breaks = models.JSONField(
        _('Дополнительные перерывы'),
        blank=True,
        null=True,
        help_text='JSON: [{"start": "10:00", "end": "10:15", "name": "Кофе-брейк"}]'
    )
    is_default = models.BooleanField(_('График по умолчанию'), default=False)
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Тип графика работы')
        verbose_name_plural = _('Типы графиков работы')
        ordering = ['-is_default', 'name']
        db_table = 'work_schedule_types'

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

    def save(self, *args, **kwargs):
        # Если это график по умолчанию, убираем флаг у остальных
        if self.is_default:
            WorkScheduleType.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class UserSchedule(models.Model):
    """График работы пользователя"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work_schedule',
        verbose_name=_('Пользователь')
    )
    schedule_type = models.ForeignKey(
        WorkScheduleType,
        on_delete=models.PROTECT,
        verbose_name=_('Тип графика')
    )
    created_at = models.DateTimeField(_('Дата назначения'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата изменения'), auto_now=True)

    class Meta:
        verbose_name = _('График пользователя')
        verbose_name_plural = _('Графики пользователей')
        db_table = 'user_schedules'

    def __str__(self):
        return f"{self.user.email} - {self.schedule_type.name}"


class Holiday(models.Model):
    """Праздничные и выходные дни"""
    date = models.DateField(_('Дата'), unique=True)
    name = models.CharField(_('Название'), max_length=255)
    is_working_day = models.BooleanField(
        _('Рабочий день'),
        default=False,
        help_text='Галочка если это перенесенный рабочий день'
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Праздник/Выходной')
        verbose_name_plural = _('Праздники и выходные')
        ordering = ['date']
        db_table = 'holidays'

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%Y')} - {self.name}"

