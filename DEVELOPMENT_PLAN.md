# План развития проекта "В плюсе" - Onboarding платформа

## Текущее состояние проекта (что уже реализовано ✅)

### 1. Базовая инфраструктура
- ✅ Django 4.2.28 + DRF
- ✅ PostgreSQL подключение через .env
- ✅ JWT авторизация (djangorestframework-simplejwt)
- ✅ Swagger документация (drf-yasg)
- ✅ CORS настроен

### 2. Модель пользователей
- ✅ CustomUser (email-based авторизация)
- ✅ Поля: first_name, last_name, position, department
- ✅ Роли через is_staff / is_superuser

### 3. API эндпоинты пользователей
- ✅ POST /api/v1/account/login/ - вход
- ✅ POST /api/v1/account/logout/ - выход
- ✅ GET /api/v1/account/me/ - текущий пользователь
- ✅ GET/PUT /api/v1/account/my_profile/ - профиль
- ✅ CRUD для админов (только superadmin)
- ✅ CRUD для стажёров (admin/superadmin)
- ✅ GET /api/v1/account/superadmin/users/ - список всех

### 4. Права доступа
- ✅ IsSuperAdmin - только суперадмин
- ✅ IsAdmin - админ или суперадмин
- ✅ IsIntern - все авторизованные

---

## Что нужно реализовать согласно ТЗ 📋

### ЭТАП 1: Расширение моделей и базовой структуры

#### 1.1. Создать новые Django приложения
```
- news/           # Новости (главная страница)
- onboarding/     # Онбординг и отчёты
- regulations/    # Регламенты
- schedule/       # График работы
- instruction/    # Инструкции
- feedback/       # Обратная связь
- notifications/  # Уведомления
```

#### 1.2. Модели для приложения `news`
- **News** - новости компании
  - title (CharField)
  - short_description (TextField)
  - full_text (TextField)
  - image (ImageField)
  - published_date (DateTimeField)
  - is_active (BooleanField)
  - order (IntegerField)

- **Employee** - сотрудники для слайдера
  - photo (ImageField)
  - full_name (CharField)
  - position (CharField)
  - department (CharField, null=True)
  - contact (CharField, max_length=30, null=True)
  - order (IntegerField)
  - is_active (BooleanField)

- **WelcomeBlock** - приветственный блок
  - title (CharField)
  - text (TextField)
  - is_active (BooleanField)

#### 1.3. Модели для приложения `onboarding`
- **OnboardingDay** - день онбординга
  - day_number (IntegerField)
  - title (CharField)
  - description (TextField)
  - goals (TextField)
  - instructions (TextField)
  - deadline_time (TimeField)
  - is_active (BooleanField)
  - order (IntegerField)

- **OnboardingMedia** - медиа для дня
  - onboarding_day (ForeignKey)
  - media_type (CharField: link/video/image/file)
  - title (CharField)
  - content (TextField/FileField)
  - order (IntegerField)

- **DailyReport** - отчёты стажёров
  - intern (ForeignKey CustomUser)
  - onboarding_day (ForeignKey)
  - what_done (TextField)
  - what_will_do (TextField)
  - problems (TextField)
  - attachment_link (URLField, null=True)
  - attachment_file (FileField, null=True)
  - status (CharField: draft/submitted/accepted/revision/rejected)
  - submitted_at (DateTimeField)
  - reviewer (ForeignKey CustomUser, null=True)
  - reviewer_comment (TextField, null=True)
  - reviewed_at (DateTimeField, null=True)

#### 1.4. Модели для приложения `regulations`
- **Regulation** - регламенты
  - title (CharField)
  - description (TextField, null=True)
  - content_type (CharField: link/file)
  - link (URLField, null=True)
  - file (FileField, null=True)
  - order (IntegerField)
  - is_active (BooleanField)

#### 1.5. Модели для приложения `schedule`
- **WorkScheduleType** - типы графиков работы
  - name (CharField)
  - description (TextField)
  - work_days (JSONField) # [1,2,3,4,5] понедельник-пятница
  - start_time (TimeField)
  - end_time (TimeField)
  - lunch_start (TimeField)
  - lunch_end (TimeField)
  - breaks (JSONField, null=True)
  - is_default (BooleanField)
  - is_active (BooleanField)

- **UserSchedule** - график пользователя
  - user (OneToOneField CustomUser)
  - schedule_type (ForeignKey WorkScheduleType)

- **Holiday** - праздничные дни
  - date (DateField)
  - name (CharField)
  - is_working_day (BooleanField default=False)

#### 1.6. Модели для приложения `instruction`
- **Instruction** - инструкция по платформе
  - title (CharField)
  - content_type (CharField: text/link/file)
  - text_content (TextField, null=True)
  - link (URLField, null=True)
  - file (FileField, null=True)
  - is_active (BooleanField)
  - updated_at (DateTimeField)

#### 1.7. Модели для приложения `feedback`
- **Feedback** - обратная связь
  - feedback_type (CharField: complaint/suggestion/review)
  - is_anonymous (BooleanField)
  - full_name (CharField, null=True)
  - contact_type (CharField: telegram/whatsapp, null=True)
  - contact_value (CharField, null=True)
  - message (TextField)
  - created_at (DateTimeField)
  - status (CharField: new/in_progress/resolved)
  - admin_comment (TextField, null=True)

#### 1.8. Модели для приложения `notifications`
- **Notification** - уведомления
  - user (ForeignKey CustomUser)
  - title (CharField)
  - message (TextField)
  - notification_type (CharField: system/educational/info)
  - is_read (BooleanField default=False)
  - created_at (DateTimeField)

---

### ЭТАП 2: API эндпоинты (по разделам ТЗ)

#### 2.1. Главная страница
```
GET  /api/v1/news/                    # Список новостей (слайдер)
GET  /api/v1/news/{id}/               # Детальная новость
GET  /api/v1/employees/               # Сотрудники (слайдер)
GET  /api/v1/welcome/                 # Приветственный блок
POST /api/v1/feedback/                # Отправка обратной связи
```

#### 2.2. Онбординг/Отчёты
```
GET  /api/v1/onboarding/days/         # Список дней онбординга
GET  /api/v1/onboarding/days/{id}/    # Детали дня
GET  /api/v1/reports/                 # Мои отчёты (стажёр)
POST /api/v1/reports/                 # Создать отчёт
GET  /api/v1/reports/{id}/            # Детали отчёта
PUT  /api/v1/reports/{id}/            # Обновить (если draft)
GET  /api/v1/reports/all/             # Все отчёты (админ)
PATCH /api/v1/reports/{id}/review/    # Проверить отчёт (админ)
```

#### 2.3. Регламенты
```
GET  /api/v1/regulations/             # Список регламентов
GET  /api/v1/regulations/{id}/        # Детали регламента
```

#### 2.4. График работы
```
GET  /api/v1/schedule/types/          # Типы графиков
GET  /api/v1/schedule/my/             # Мой график
PUT  /api/v1/schedule/my/             # Выбрать график
GET  /api/v1/schedule/calendar/       # Календарь месяца
GET  /api/v1/schedule/holidays/       # Праздники
```

#### 2.5. Инструкция
```
GET  /api/v1/instruction/             # Инструкция платформы
```

#### 2.6. Уведомления
```
GET  /api/v1/notifications/           # Мои уведомления
PATCH /api/v1/notifications/{id}/read/ # Отметить прочитанным
```

---

### ЭТАП 3: Админ-панель (Django Admin)

Для каждой модели настроить:
- Удобный list_display
- Фильтры и поиск
- Inline редактирование связанных объектов
- Drag-and-drop сортировку (order)
- Права доступа по ролям

---

### ЭТАП 4: Frontend (не входит в текущий бэкенд проект)

Отдельный фронтенд (React/Vue/Angular) будет:
- Потреблять API
- Реализовывать Header, Footer, Sidebar
- Страницы по ТЗ
- Авторизация JWT
- Мультиязычность (RU/EN/KG)

---

## Приоритеты реализации

### Спринт 1 (Базовые модели и API)
1. Создать приложения
2. Модели: News, Employee, WelcomeBlock, Feedback
3. API главной страницы
4. Расширить модель CustomUser (добавить аватар если нужно)

### Спринт 2 (Онбординг)
1. Модели OnboardingDay, OnboardingMedia, DailyReport
2. API онбординга и отчётов
3. Логика статусов и проверки

### Спринт 3 (Регламенты, График, Инструкции)
1. Модели Regulation, WorkScheduleType, Instruction
2. API для этих разделов
3. Календарь и праздники

### Спринт 4 (Уведомления и доработки)
1. Модель Notification
2. Система уведомлений
3. Интеграция уведомлений в процессы

### Спринт 5 (Тестирование и оптимизация)
1. Полное тестирование API
2. Документация Swagger
3. Оптимизация запросов

---

## Технические детали

### Зависимости (дополнительно)
```
Pillow              # для ImageField
django-filter       # фильтрация в API
django-cors-headers # уже есть
```

### Структура файлов
```
onboarding/
├── account/         # уже есть - пользователи
├── news/            # новое
├── onboarding_app/  # новое (онбординг)
├── regulations/     # новое
├── schedule/        # новое
├── instruction/     # новое
├── feedback/        # новое
├── notifications/   # новое
├── onboard/         # settings, urls
└── manage.py
```

---

## Следующие шаги

1. Согласовать план с командой
2. Начать со спринта 1
3. Создать миграции
4. Разработать API
5. Протестировать через Swagger
6. Передать фронтенду документацию API

