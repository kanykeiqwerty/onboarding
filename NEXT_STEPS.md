# Следующие шаги - Спринт 2: Онбординг и отчёты

## Что нужно сделать дальше

### 1. Создать приложение для онбординга
```bash
python manage.py startapp onboarding_app
```

### 2. Модели для онбординга

#### OnboardingDay (День онбординга)
```python
class OnboardingDay(models.Model):
    day_number = IntegerField()
    title = CharField(max_length=255)  # "День 1. Знакомство"
    description = TextField()  # Описание целей дня
    instructions = TextField()  # Текстовые инструкции
    deadline_time = TimeField()  # Дедлайн в формате ЧЧ:ММ
    is_active = BooleanField(default=True)
    order = IntegerField(default=0)
```

#### OnboardingMedia (Медиа-материалы)
```python
class OnboardingMedia(models.Model):
    MEDIA_TYPES = [
        ('link', 'Ссылка'),
        ('video', 'Видео (YouTube/Vimeo)'),
        ('image', 'Изображение'),
        ('file', 'Файл'),
    ]
    
    onboarding_day = ForeignKey(OnboardingDay)
    media_type = CharField(choices=MEDIA_TYPES)
    title = CharField(max_length=255)
    link = URLField(null=True, blank=True)
    file = FileField(null=True, blank=True)
    order = IntegerField(default=0)
```

#### DailyReport (Отчёт стажёра)
```python
class DailyReport(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'Отправлен'),
        ('accepted', 'Принят'),
        ('revision', 'На доработку'),
        ('rejected', 'Отклонён'),
    ]
    
    intern = ForeignKey(CustomUser, related_name='reports')
    onboarding_day = ForeignKey(OnboardingDay)
    
    # Поля отчёта
    what_done = TextField()  # Что сделал
    what_will_do = TextField()  # Что буду делать
    problems = TextField()  # Какие проблемы
    attachment_link = URLField(null=True, blank=True)
    attachment_file = FileField(null=True, blank=True)
    
    # Метаданные
    status = CharField(choices=STATUS_CHOICES, default='draft')
    submitted_at = DateTimeField(null=True, blank=True)
    
    # Проверка
    reviewer = ForeignKey(CustomUser, null=True, related_name='reviewed_reports')
    reviewer_comment = TextField(null=True, blank=True)
    reviewed_at = DateTimeField(null=True, blank=True)
```

### 3. API эндпоинты

```python
# Для стажёров
GET  /api/v1/onboarding/days/          # Список дней
GET  /api/v1/onboarding/days/{id}/     # Детали дня + материалы
GET  /api/v1/reports/my/               # Мои отчёты
POST /api/v1/reports/                  # Создать отчёт
PUT  /api/v1/reports/{id}/             # Обновить черновик
POST /api/v1/reports/{id}/submit/      # Отправить на проверку

# Для админов
GET   /api/v1/reports/all/             # Все отчёты
PATCH /api/v1/reports/{id}/review/     # Проверить отчёт
```

### 4. Логика проверки отчётов

**Валидация при отправке:**
- Все три поля (что сделал, что буду делать, проблемы) обязательны
- Если пусто → автоматически статус "rejected"

**Проверка админом:**
```python
@action(detail=True, methods=['patch'])
def review(self, request, pk=None):
    report = self.get_object()
    action = request.data.get('action')  # 'accept' или 'revision'
    comment = request.data.get('comment', '')
    
    if action == 'accept':
        report.status = 'accepted'
    elif action == 'revision':
        if not comment:
            return Response({'error': 'Комментарий обязателен'}, status=400)
        report.status = 'revision'
    
    report.reviewer = request.user
    report.reviewer_comment = comment
    report.reviewed_at = timezone.now()
    report.save()
    
    # Отправить уведомление стажёру
    
    return Response({'message': 'Отчёт проверен'})
```

### 5. Приоритетные задачи

**Задача 1:** Создать модели OnboardingDay, OnboardingMedia, DailyReport  
**Задача 2:** Создать serializers для онбординга  
**Задача 3:** Создать ViewSets с правами доступа  
**Задача 4:** Настроить админ-панель для управления днями  
**Задача 5:** Добавить логику статусов и валидации  
**Задача 6:** Интегрировать с системой уведомлений  

### 6. Регламенты и график (Спринт 3)

После онбординга создать:

**Приложение regulations:**
```python
class Regulation(models.Model):
    title = CharField()
    description = TextField()
    content_type = CharField(choices=[('link', 'Ссылка'), ('file', 'Файл')])
    link = URLField(null=True)
    file = FileField(null=True)
    order = IntegerField()
    is_active = BooleanField()
```

**Приложение schedule:**
```python
class WorkScheduleType(models.Model):
    name = CharField()  # "График 5/2"
    description = TextField()
    work_days = JSONField()  # [1,2,3,4,5]
    start_time = TimeField()  # 09:00
    end_time = TimeField()  # 18:00
    lunch_start = TimeField()  # 13:00
    lunch_end = TimeField()  # 14:00
    is_default = BooleanField()

class UserSchedule(models.Model):
    user = OneToOneField(CustomUser)
    schedule_type = ForeignKey(WorkScheduleType)

class Holiday(models.Model):
    date = DateField()
    name = CharField()
    is_working_day = BooleanField(default=False)
```

### 7. Команды для быстрого старта Спринта 2

```bash
# 1. Создать приложение
python manage.py startapp onboarding_app

# 2. Добавить в INSTALLED_APPS

# 3. Создать модели (см. выше)

# 4. Создать миграции
python manage.py makemigrations
python manage.py migrate

# 5. Зарегистрировать в админке

# 6. Создать serializers и views

# 7. Подключить URLs

# 8. Протестировать через Swagger
```

### 8. Полезные ссылки

- **Swagger:** http://127.0.0.1:8000/api/v1/docs/
- **Admin:** http://127.0.0.1:8000/admin/
- **План развития:** DEVELOPMENT_PLAN.md
- **README:** README.md

---

**Текущий статус:** Спринт 1 завершён ✅  
**Следующий шаг:** Начать Спринт 2 - Онбординг и отчёты

