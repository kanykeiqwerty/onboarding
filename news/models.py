from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    """Модель новостей для главной страницы (слайдер)"""
    title = models.CharField(_('Заголовок'), max_length=255)
    short_description = models.TextField(_('Краткое описание'), help_text='1 предложение для карточки')
    full_text = models.TextField(_('Полный текст новости'))
    image = models.ImageField(_('Изображение'), upload_to='news/', blank=True, null=True)
    published_date = models.DateTimeField(_('Дата публикации'), auto_now_add=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    order = models.IntegerField(_('Порядок отображения'), default=0, help_text='Чем меньше число, тем выше в списке')
    
    class Meta:
        verbose_name = _('Новость')
        verbose_name_plural = _('Новости')
        ordering = ['order', '-published_date']
        db_table = 'news'
    
    def __str__(self):
        return self.title


class Employee(models.Model):
    """Модель сотрудников для слайдера на главной странице"""
    photo = models.ImageField(_('Фотография'), upload_to='employees/', blank=True, null=True)
    full_name = models.CharField(_('ФИО'), max_length=255)
    position = models.CharField(_('Должность'), max_length=255)
    department = models.CharField(_('Подразделение'), max_length=255, blank=True, null=True)
    contact = models.CharField(_('Контакт'), max_length=30, blank=True, null=True, 
                               help_text='До 30 символов, в свободной форме')
    order = models.IntegerField(_('Порядок отображения'), default=0)
    is_active = models.BooleanField(_('Активен'), default=True)
    
    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')
        ordering = ['order', 'full_name']
        db_table = 'employees'
    
    def __str__(self):
        return f"{self.full_name} - {self.position}"


class WelcomeBlock(models.Model):
    """Приветственный блок на главной странице"""
    title = models.CharField(_('Заголовок'), max_length=255)
    text = models.TextField(_('Текст приветствия'))
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлён'), auto_now=True)
    
    class Meta:
        verbose_name = _('Приветственный блок')
        verbose_name_plural = _('Приветственные блоки')
        db_table = 'welcome_blocks'
    
    def __str__(self):
        return self.title
