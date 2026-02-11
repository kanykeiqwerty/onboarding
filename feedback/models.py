from django.db import models
from django.utils.translation import gettext_lazy as _


class Feedback(models.Model):
    """Модель обратной связи от пользователей"""

    FEEDBACK_TYPES = [
        ('complaint', _('Жалоба')),
        ('suggestion', _('Предложение')),
        ('review', _('Отзыв')),
    ]

    CONTACT_TYPES = [
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]

    STATUS_CHOICES = [
        ('new', _('Новое')),
        ('in_progress', _('В обработке')),
        ('resolved', _('Решено')),
    ]

    feedback_type = models.CharField(_('Тип обращения'), max_length=20, choices=FEEDBACK_TYPES)
    is_anonymous = models.BooleanField(_('Анонимное'), default=False)

    # Поля для неанонимной формы
    full_name = models.CharField(_('ФИО'), max_length=255, blank=True, null=True)
    contact_type = models.CharField(_('Тип контакта'), max_length=20, choices=CONTACT_TYPES,
                                   blank=True, null=True)
    contact_value = models.CharField(_('Контакт'), max_length=255, blank=True, null=True)

    message = models.TextField(_('Сообщение'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    status = models.CharField(_('Статус'), max_length=20, choices=STATUS_CHOICES, default='new')
    admin_comment = models.TextField(_('Комментарий администратора'), blank=True, null=True)

    class Meta:
        verbose_name = _('Обратная связь')
        verbose_name_plural = _('Обратная связь')
        ordering = ['-created_at']
        db_table = 'feedback'

    def __str__(self):
        return f"{self.get_feedback_type_display()} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"

