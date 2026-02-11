from django.db import models
from django.utils.translation import gettext_lazy as _


class Regulation(models.Model):
    """Модель регламентов компании"""
    CONTENT_TYPES = [
        ('link', _('Ссылка')),
        ('file', _('Файл')),
    ]

    title = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'), blank=True, null=True)
    content_type = models.CharField(_('Тип контента'), max_length=10, choices=CONTENT_TYPES)
    link = models.URLField(_('Ссылка'), blank=True, null=True)
    file = models.FileField(_('Файл'), upload_to='regulations/', blank=True, null=True)
    order = models.IntegerField(_('Порядок отображения'), default=0)
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Регламент')
        verbose_name_plural = _('Регламенты')
        ordering = ['order', 'title']
        db_table = 'regulations'

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.content_type == 'link' and not self.link:
            raise ValidationError({'link': 'Ссылка обязательна для типа "Ссылка"'})
        if self.content_type == 'file' and not self.file:
            raise ValidationError({'file': 'Файл обязателен для типа "Файл"'})

