from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class OnboardingDay(models.Model):
    """Модель дня онбординга"""
    day_number = models.IntegerField(_('Номер дня'), unique=True)
    title = models.CharField(_('Название'), max_length=255, help_text='Например: День 1. Знакомство с компанией')
    description = models.TextField(_('Описание целей дня'))
    instructions = models.TextField(_('Текстовые инструкции'))
    deadline_time = models.TimeField(_('Дедлайн сдачи отчёта'), help_text='Формат ЧЧ:ММ')
    is_active = models.BooleanField(_('Активен'), default=True)
    order = models.IntegerField(_('Порядок отображения'), default=0)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('День онбординга')
        verbose_name_plural = _('Дни онбординга')
        ordering = ['order', 'day_number']
        db_table = 'onboarding_days'

    def __str__(self):
        return f"День {self.day_number}. {self.title}"


class OnboardingMedia(models.Model):
    """Медиа-материалы для дня онбординга"""
    MEDIA_TYPES = [
        ('link', _('Ссылка')),
        ('video', _('Видео (YouTube/Vimeo)')),
        ('image', _('Изображение')),
        ('file', _('Файл')),
    ]

    onboarding_day = models.ForeignKey(
        OnboardingDay,
        on_delete=models.CASCADE,
        related_name='media_materials',
        verbose_name=_('День онбординга')
    )
    media_type = models.CharField(_('Тип материала'), max_length=20, choices=MEDIA_TYPES)
    title = models.CharField(_('Название'), max_length=255)
    link = models.URLField(_('Ссылка'), blank=True, null=True)
    file = models.FileField(_('Файл'), upload_to='onboarding/media/', blank=True, null=True)
    order = models.IntegerField(_('Порядок отображения'), default=0)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Медиа-материал')
        verbose_name_plural = _('Медиа-материалы')
        ordering = ['order', 'created_at']
        db_table = 'onboarding_media'

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()}) - День {self.onboarding_day.day_number}"

    def clean(self):
        """Валидация: должна быть либо ссылка, либо файл"""
        from django.core.exceptions import ValidationError
        if self.media_type == 'link' and not self.link:
            raise ValidationError({'link': 'Ссылка обязательна для типа "Ссылка"'})
        if self.media_type in ['image', 'file'] and not self.file:
            raise ValidationError({'file': 'Файл обязателен для выбранного типа'})


class DailyReport(models.Model):
    """Ежедневный отчёт стажёра"""
    STATUS_CHOICES = [
        ('draft', _('Черновик')),
        ('submitted', _('Отправлен')),
        ('accepted', _('Принят')),
        ('revision', _('На доработку')),
        ('rejected', _('Отклонён')),
    ]

    # Основная информация
    intern = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_reports',
        verbose_name=_('Стажёр')
    )
    onboarding_day = models.ForeignKey(
        OnboardingDay,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('День онбординга')
    )

    # Поля отчёта
    what_done = models.TextField(_('Что сделал'), blank=True)
    what_will_do = models.TextField(_('Что буду делать'), blank=True)
    problems = models.TextField(_('Какие проблемы возникли'), blank=True)
    attachment_link = models.URLField(_('Ссылка на результат'), blank=True, null=True)
    attachment_file = models.FileField(
        _('Файл с результатом'),
        upload_to='onboarding/reports/',
        blank=True,
        null=True
    )

    # Метаданные
    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    submitted_at = models.DateTimeField(_('Дата отправки'), blank=True, null=True)

    # Проверка
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='reviewed_reports',
        verbose_name=_('Проверяющий'),
        blank=True,
        null=True
    )
    reviewer_comment = models.TextField(_('Комментарий проверяющего'), blank=True, null=True)
    reviewed_at = models.DateTimeField(_('Дата проверки'), blank=True, null=True)

    class Meta:
        verbose_name = _('Ежедневный отчёт')
        verbose_name_plural = _('Ежедневные отчёты')
        ordering = ['-created_at']
        db_table = 'daily_reports'
        unique_together = ['intern', 'onboarding_day']  # Один отчёт на день на стажёра

    def __str__(self):
        return f"Отчёт {self.intern.email} - День {self.onboarding_day.day_number} ({self.get_status_display()})"

    def is_empty(self):
        """Проверка, пустой ли отчёт"""
        return not (self.what_done.strip() and self.what_will_do.strip() and self.problems.strip())

    def submit(self):
        """Отправка отчёта на проверку"""
        if self.is_empty():
            self.status = 'rejected'
        else:
            self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save()

    def accept(self, reviewer, comment=''):
        """Принять отчёт"""
        self.status = 'accepted'
        self.reviewer = reviewer
        self.reviewer_comment = comment
        self.reviewed_at = timezone.now()
        self.save()

    def request_revision(self, reviewer, comment):
        """Отправить на доработку"""
        self.status = 'revision'
        self.reviewer = reviewer
        self.reviewer_comment = comment
        self.reviewed_at = timezone.now()
        self.save()

    def reject(self, reviewer, comment=''):
        """Отклонить отчёт"""
        self.status = 'rejected'
        self.reviewer = reviewer
        self.reviewer_comment = comment
        self.reviewed_at = timezone.now()
        self.save()

