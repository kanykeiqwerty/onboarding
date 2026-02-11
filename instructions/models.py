from django.db import models
from django.utils.translation import gettext_lazy as _


class Instruction(models.Model):
    """Инструкция по использованию платформы"""
    CONTENT_TYPES = [
        ('text', _('Текст')),
        ('link', _('Ссылка')),
        ('file', _('Файл')),
    ]

    title = models.CharField(_('Заголовок'), max_length=255)
    content_type = models.CharField(_('Тип контента'), max_length=10, choices=CONTENT_TYPES)
    text_content = models.TextField(_('Текстовое содержимое'), blank=True, null=True)
    link = models.URLField(_('Ссылка'), blank=True, null=True)
    file = models.FileField(_('Файл'), upload_to='instructions/', blank=True, null=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Инструкция')
        verbose_name_plural = _('Инструкции')
        db_table = 'instructions'

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.content_type == 'text' and not self.text_content:
            raise ValidationError({'text_content': 'Текст обязателен для типа "Текст"'})
        if self.content_type == 'link' and not self.link:
            raise ValidationError({'link': 'Ссылка обязательна для типа "Ссылка"'})
        if self.content_type == 'file' and not self.file:
            raise ValidationError({'file': 'Файл обязателен для типа "Файл"'})

