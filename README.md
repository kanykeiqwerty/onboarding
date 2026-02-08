# Onboarding Platform "В плюсе" - Backend API

## Описание проекта

Backend API для корпоративной onboarding-платформы компании "В плюсе". Платформа предназначена для автоматизации процесса адаптации стажёров, централизации регламентов и снижения управленческой нагрузки.

## Технологический стек

- **Python 3.x**
- **Django 5.2.11**
- **Django REST Framework**
- **PostgreSQL**
- **JWT авторизация** (djangorestframework-simplejwt)
- **Swagger/OpenAPI** (drf-yasg)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd onboarding
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
```

### 3. Активация виртуального окружения

**Windows (cmd.exe):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 6. Применение миграций
```bash
python manage.py migrate
```

### 7. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 8. Запуск сервера
```bash
python manage.py runserver 8000
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## Доступы

### Swagger документация
- **URL:** http://127.0.0.1:8000/api/v1/docs/
- Интерактивная документация всех API эндпоинтов

### Django Admin панель
- **URL:** http://127.0.0.1:8000/admin/
- Управление контентом и пользователями

## Текущие API эндпоинты

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/v1/account/login/` | Вход (получение JWT токенов) |
| POST | `/api/v1/account/logout/` | Выход (blacklist refresh token) |

### Пользователи

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/account/me/` | Текущий пользователь | Авторизованные |
| GET/PUT | `/api/v1/account/my_profile/` | Мой профиль | Авторизованные |
| POST | `/api/v1/account/admin/create/` | Создать админа | Суперадмин |
| GET | `/api/v1/account/admin/list/` | Список админов | Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/admin/{id}/` | Управление админом | Суперадмин |
| POST | `/api/v1/account/intern/create/` | Создать стажёра | Админ/Суперадмин |
| GET | `/api/v1/account/intern/list/` | Список стажёров | Админ/Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/intern/{id}/` | Управление стажёром | Админ/Суперадмин |
| GET | `/api/v1/account/superadmin/users/` | Все пользователи | Суперадмин |
| PUT | `/api/v1/account/superadmin/users/{id}/` | Изменить роль | Суперадмин |

### Главная страница

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/news/` | Список новостей (слайдер) | Авторизованные |
| GET | `/api/v1/news/{id}/` | Детали новости (лайтбокс) | Авторизованные |
| GET | `/api/v1/employees/` | Сотрудники (слайдер) | Авторизованные |
| GET | `/api/v1/welcome/` | Приветственный блок | Авторизованные |

### Обратная связь

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/v1/feedback/` | Отправить обратную связь | Авторизованные |
| GET | `/api/v1/feedback/` | Список обращений | Админ/Суперадмин |
| GET | `/api/v1/feedback/{id}/` | Детали обращения | Админ/Суперадмин |
| PATCH | `/api/v1/feedback/{id}/` | Обновить статус | Админ/Суперадмин |

## Роли пользователей

### 1. Стажёр (intern)
- `is_staff=False`, `is_superuser=False`
- Доступ к обучающим материалам и регламентам
- Может просматривать свой профиль и обновлять данные
- Может отправлять обратную связь

### 2. Администратор (admin)
- `is_staff=True`, `is_superuser=False`
- Управление контентом платформы
- Создание и управление стажёрами
- Проверка отчётов стажёров
- Просмотр обратной связи

### 3. Суперадминистратор (superadmin)
- `is_staff=True`, `is_superuser=True`
- Полный доступ ко всем функциям
- Управление администраторами
- Изменение ролей пользователей
- Системные настройки

## Структура проекта

```
onboarding/
├── account/              # Пользователи и авторизация
│   ├── migrations/
│   ├── serializers/
│   ├── views/
│   ├── models.py
│   ├── permission.py
│   └── urls.py
├── news/                 # Новости, сотрудники, приветствие
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── feedback/             # Обратная связь
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── onboard/              # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                # Загруженные файлы
├── static/               # Статические файлы
├── .env                  # Переменные окружения (не в Git!)
├── .gitignore
├── requirements.txt
├── manage.py
├── DEVELOPMENT_PLAN.md   # План развития проекта
└── README.md             # Этот файл
```

## План развития (Roadmap)

См. подробный план в файле `DEVELOPMENT_PLAN.md`

### ✅ Спринт 1 - ВЫПОЛНЕН
- Базовая авторизация и управление пользователями
- Модели для главной страницы (новости, сотрудники, приветствие)
- API для обратной связи

### 🔄 Спринт 2 - В РАЗРАБОТКЕ
- Модели онбординга (дни, материалы, отчёты)
- API для прохождения онбординга
- Система проверки отчётов

### 📋 Спринт 3 - ЗАПЛАНИРОВАН
- Регламенты и инструкции
- График работы и календарь
- Управление через админ-панель

### 📋 Спринт 4 - ЗАПЛАНИРОВАН
- Система уведомлений
- Интеграция уведомлений в процессы
- Расширенная аналитика

## Модели данных

### CustomUser
- `email` - уникальный email (используется для входа)
- `first_name`, `last_name` - ФИО
- `position` - должность (Backend/Frontend/PM/Design)
- `department` - подразделение (IT/Other)
- `is_staff` - признак администратора
- `is_superuser` - признак суперадмина

### News
- `title` - заголовок новости
- `short_description` - краткое описание для карточки
- `full_text` - полный текст
- `image` - изображение
- `is_active` - активна ли новость
- `order` - порядок отображения

### Employee
- `photo` - фотография сотрудника
- `full_name` - ФИО
- `position` - должность
- `department` - подразделение
- `contact` - контакт (до 30 символов)
- `order` - порядок в слайдере

### WelcomeBlock
- `title` - заголовок приветствия
- `text` - текст приветствия
- `is_active` - активен ли блок

### Feedback
- `feedback_type` - тип (жалоба/предложение/отзыв)
- `is_anonymous` - анонимное ли обращение
- `full_name` - ФИО (для неанонимных)
- `contact_type` - тип контакта (Telegram/WhatsApp)
- `contact_value` - значение контакта
- `message` - текст обращения
- `status` - статус (новое/в обработке/решено)
- `admin_comment` - комментарий администратора

## Авторизация JWT

### Получение токенов
```bash
POST /api/v1/account/login/
{
  "email": "user@example.com",
  "password": "password"
}
```

**Ответ:**
```json
{
  "refresh": "...",
  "access": "...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "intern",
    "first_name": "Иван",
    "last_name": "Иванов"
  }
}
```

### Использование токена
Добавьте заголовок в каждый запрос:
```
Authorization: Bearer <access_token>
```

или в Swagger:
```
Authorization: JWT <access_token>
```

## Тестирование API

### Через Swagger UI
1. Откройте http://127.0.0.1:8000/api/v1/docs/
2. Нажмите "Authorize" справа вверху
3. Введите: `Bearer <ваш_access_token>`
4. Тестируйте эндпоинты

### Через Postman/Insomnia
1. Импортируйте OpenAPI схему: http://127.0.0.1:8000/api/v1/docs/?format=openapi
2. Настройте авторизацию Bearer Token
3. Выполняйте запросы

## Разработка

### Создание новой миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание нового приложения
```bash
python manage.py startapp app_name
```
Не забудьте добавить в `INSTALLED_APPS`!

### Сбор статики
```bash
python manage.py collectstatic
```

## Поддержка и контакты

Для вопросов по проекту обращайтесь к команде разработки.

---

**Статус проекта:** В активной разработке  
**Версия:** 0.3.5  
**Дата обновления:** 08.02.2026  
**Готовность:** Backend 90%, Frontend 100% (тестовый)
# Onboarding Platform "В плюсе" - Backend API

## Описание проекта

Backend API для корпоративной onboarding-платформы компании "В плюсе". Платформа предназначена для автоматизации процесса адаптации стажёров, централизации регламентов и снижения управленческой нагрузки.

## Технологический стек

- **Python 3.x**
- **Django 5.2.11**
- **Django REST Framework**
- **PostgreSQL**
- **JWT авторизация** (djangorestframework-simplejwt)
- **Swagger/OpenAPI** (drf-yasg)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd onboarding
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
```

### 3. Активация виртуального окружения

**Windows (cmd.exe):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 6. Применение миграций
```bash
python manage.py migrate
```

### 7. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 8. Запуск сервера
```bash
python manage.py runserver 8000
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## Доступы

### Swagger документация
- **URL:** http://127.0.0.1:8000/api/v1/docs/
- Интерактивная документация всех API эндпоинтов

### Django Admin панель
- **URL:** http://127.0.0.1:8000/admin/
- Управление контентом и пользователями

## Текущие API эндпоинты

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/v1/account/login/` | Вход (получение JWT токенов) |
| POST | `/api/v1/account/logout/` | Выход (blacklist refresh token) |

### Пользователи

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/account/me/` | Текущий пользователь | Авторизованные |
| GET/PUT | `/api/v1/account/my_profile/` | Мой профиль | Авторизованные |
| POST | `/api/v1/account/admin/create/` | Создать админа | Суперадмин |
| GET | `/api/v1/account/admin/list/` | Список админов | Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/admin/{id}/` | Управление админом | Суперадмин |
| POST | `/api/v1/account/intern/create/` | Создать стажёра | Админ/Суперадмин |
| GET | `/api/v1/account/intern/list/` | Список стажёров | Админ/Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/intern/{id}/` | Управление стажёром | Админ/Суперадмин |
| GET | `/api/v1/account/superadmin/users/` | Все пользователи | Суперадмин |
| PUT | `/api/v1/account/superadmin/users/{id}/` | Изменить роль | Суперадмин |

### Главная страница

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/news/` | Список новостей (слайдер) | Авторизованные |
| GET | `/api/v1/news/{id}/` | Детали новости (лайтбокс) | Авторизованные |
| GET | `/api/v1/employees/` | Сотрудники (слайдер) | Авторизованные |
| GET | `/api/v1/welcome/` | Приветственный блок | Авторизованные |

### Обратная связь

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/v1/feedback/` | Отправить обратную связь | Авторизованные |
| GET | `/api/v1/feedback/` | Список обращений | Админ/Суперадмин |
| GET | `/api/v1/feedback/{id}/` | Детали обращения | Админ/Суперадмин |
| PATCH | `/api/v1/feedback/{id}/` | Обновить статус | Админ/Суперадмин |

## Роли пользователей

### 1. Стажёр (intern)
- `is_staff=False`, `is_superuser=False`
- Доступ к обучающим материалам и регламентам
- Может просматривать свой профиль и обновлять данные
- Может отправлять обратную связь

### 2. Администратор (admin)
- `is_staff=True`, `is_superuser=False`
- Управление контентом платформы
- Создание и управление стажёрами
- Проверка отчётов стажёров
- Просмотр обратной связи

### 3. Суперадминистратор (superadmin)
- `is_staff=True`, `is_superuser=True`
- Полный доступ ко всем функциям
- Управление администраторами
- Изменение ролей пользователей
- Системные настройки

## Структура проекта

```
onboarding/
├── account/              # Пользователи и авторизация
│   ├── migrations/
│   ├── serializers/
│   ├── views/
│   ├── models.py
│   ├── permission.py
│   └── urls.py
├── news/                 # Новости, сотрудники, приветствие
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── feedback/             # Обратная связь
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── onboard/              # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                # Загруженные файлы
├── static/               # Статические файлы
├── .env                  # Переменные окружения (не в Git!)
├── .gitignore
├── requirements.txt
├── manage.py
├── DEVELOPMENT_PLAN.md   # План развития проекта
└── README.md             # Этот файл
```

## План развития (Roadmap)

См. подробный план в файле `DEVELOPMENT_PLAN.md`

### ✅ Спринт 1 - ВЫПОЛНЕН
- Базовая авторизация и управление пользователями
- Модели для главной страницы (новости, сотрудники, приветствие)
- API для обратной связи

### 🔄 Спринт 2 - В РАЗРАБОТКЕ
- Модели онбординга (дни, материалы, отчёты)
- API для прохождения онбординга
- Система проверки отчётов

### 📋 Спринт 3 - ЗАПЛАНИРОВАН
- Регламенты и инструкции
- График работы и календарь
- Управление через админ-панель

### 📋 Спринт 4 - ЗАПЛАНИРОВАН
- Система уведомлений
- Интеграция уведомлений в процессы
- Расширенная аналитика

## Модели данных

### CustomUser
- `email` - уникальный email (используется для входа)
- `first_name`, `last_name` - ФИО
- `position` - должность (Backend/Frontend/PM/Design)
- `department` - подразделение (IT/Other)
- `is_staff` - признак администратора
- `is_superuser` - признак суперадмина

### News
- `title` - заголовок новости
- `short_description` - краткое описание для карточки
- `full_text` - полный текст
- `image` - изображение
- `is_active` - активна ли новость
- `order` - порядок отображения

### Employee
- `photo` - фотография сотрудника
- `full_name` - ФИО
- `position` - должность
- `department` - подразделение
- `contact` - контакт (до 30 символов)
- `order` - порядок в слайдере

### WelcomeBlock
- `title` - заголовок приветствия
- `text` - текст приветствия
- `is_active` - активен ли блок

### Feedback
- `feedback_type` - тип (жалоба/предложение/отзыв)
- `is_anonymous` - анонимное ли обращение
- `full_name` - ФИО (для неанонимных)
- `contact_type` - тип контакта (Telegram/WhatsApp)
- `contact_value` - значение контакта
- `message` - текст обращения
- `status` - статус (новое/в обработке/решено)
- `admin_comment` - комментарий администратора

## Авторизация JWT

### Получение токенов
```bash
POST /api/v1/account/login/
{
  "email": "user@example.com",
  "password": "password"
}
```

**Ответ:**
```json
{
  "refresh": "...",
  "access": "...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "intern",
    "first_name": "Иван",
    "last_name": "Иванов"
  }
}
```

### Использование токена
Добавьте заголовок в каждый запрос:
```
Authorization: Bearer <access_token>
```

или в Swagger:
```
Authorization: JWT <access_token>
```

## Тестирование API

### Через Swagger UI
1. Откройте http://127.0.0.1:8000/api/v1/docs/
2. Нажмите "Authorize" справа вверху
3. Введите: `Bearer <ваш_access_token>`
4. Тестируйте эндпоинты

### Через Postman/Insomnia
1. Импортируйте OpenAPI схему: http://127.0.0.1:8000/api/v1/docs/?format=openapi
2. Настройте авторизацию Bearer Token
3. Выполняйте запросы

## Разработка

### Создание новой миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание нового приложения
```bash
python manage.py startapp app_name
```
Не забудьте добавить в `INSTALLED_APPS`!

### Сбор статики
```bash
python manage.py collectstatic
```

## Поддержка и контакты

Для вопросов по проекту обращайтесь к команде разработки.

---

**Статус проекта:** В активной разработке
**Версия:** 0.2.0 (Спринт 2 завершён)
# Onboarding Platform "В плюсе" - Backend API

## Описание проекта

Backend API для корпоративной onboarding-платформы компании "В плюсе". Платформа предназначена для автоматизации процесса адаптации стажёров, централизации регламентов и снижения управленческой нагрузки.

## Технологический стек

- **Python 3.x**
- **Django 5.2.11**
- **Django REST Framework**
- **PostgreSQL**
- **JWT авторизация** (djangorestframework-simplejwt)
- **Swagger/OpenAPI** (drf-yasg)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd onboarding
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
```

### 3. Активация виртуального окружения

**Windows (cmd.exe):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 6. Применение миграций
```bash
python manage.py migrate
```

### 7. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 8. Запуск сервера
```bash
python manage.py runserver 8000
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## Доступы

### Swagger документация
- **URL:** http://127.0.0.1:8000/api/v1/docs/
- Интерактивная документация всех API эндпоинтов

### Django Admin панель
- **URL:** http://127.0.0.1:8000/admin/
- Управление контентом и пользователями

## Текущие API эндпоинты

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/v1/account/login/` | Вход (получение JWT токенов) |
| POST | `/api/v1/account/logout/` | Выход (blacklist refresh token) |

### Пользователи

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/account/me/` | Текущий пользователь | Авторизованные |
| GET/PUT | `/api/v1/account/my_profile/` | Мой профиль | Авторизованные |
| POST | `/api/v1/account/admin/create/` | Создать админа | Суперадмин |
| GET | `/api/v1/account/admin/list/` | Список админов | Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/admin/{id}/` | Управление админом | Суперадмин |
| POST | `/api/v1/account/intern/create/` | Создать стажёра | Админ/Суперадмин |
| GET | `/api/v1/account/intern/list/` | Список стажёров | Админ/Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/intern/{id}/` | Управление стажёром | Админ/Суперадмин |
| GET | `/api/v1/account/superadmin/users/` | Все пользователи | Суперадмин |
| PUT | `/api/v1/account/superadmin/users/{id}/` | Изменить роль | Суперадмин |

### Главная страница

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/news/` | Список новостей (слайдер) | Авторизованные |
| GET | `/api/v1/news/{id}/` | Детали новости (лайтбокс) | Авторизованные |
| GET | `/api/v1/employees/` | Сотрудники (слайдер) | Авторизованные |
| GET | `/api/v1/welcome/` | Приветственный блок | Авторизованные |

### Обратная связь

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/v1/feedback/` | Отправить обратную связь | Авторизованные |
| GET | `/api/v1/feedback/` | Список обращений | Админ/Суперадмин |
| GET | `/api/v1/feedback/{id}/` | Детали обращения | Админ/Суперадмин |
| PATCH | `/api/v1/feedback/{id}/` | Обновить статус | Админ/Суперадмин |

## Роли пользователей

### 1. Стажёр (intern)
- `is_staff=False`, `is_superuser=False`
- Доступ к обучающим материалам и регламентам
- Может просматривать свой профиль и обновлять данные
- Может отправлять обратную связь

### 2. Администратор (admin)
- `is_staff=True`, `is_superuser=False`
- Управление контентом платформы
- Создание и управление стажёрами
- Проверка отчётов стажёров
- Просмотр обратной связи

### 3. Суперадминистратор (superadmin)
- `is_staff=True`, `is_superuser=True`
- Полный доступ ко всем функциям
- Управление администраторами
- Изменение ролей пользователей
- Системные настройки

## Структура проекта

```
onboarding/
├── account/              # Пользователи и авторизация
│   ├── migrations/
│   ├── serializers/
│   ├── views/
│   ├── models.py
│   ├── permission.py
│   └── urls.py
├── news/                 # Новости, сотрудники, приветствие
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── feedback/             # Обратная связь
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── onboarding_app/       # Онбординг и отчёты
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── onboard/              # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                # Загруженные файлы
├── static/               # Статические файлы
├── .env                  # Переменные окружения (не в Git!)
├── .gitignore
├── requirements.txt
├── manage.py
├── DEVELOPMENT_PLAN.md   # План развития проекта
└── README.md             # Этот файл
```

## План развития (Roadmap)

См. подробный план в файле `DEVELOPMENT_PLAN.md`

### ✅ Спринт 1 - ВЫПОЛНЕН
- Базовая авторизация и управление пользователями
- Модели для главной страницы (новости, сотрудники, приветствие)
- API для обратной связи

### 🔄 Спринт 2 - В РАЗРАБОТКЕ
- Модели онбординга (дни, материалы, отчёты)
- API для прохождения онбординга
- Система проверки отчётов

### 📋 Спринт 3 - ЗАПЛАНИРОВАН
- Регламенты и инструкции
- График работы и календарь
- Управление через админ-панель

### 📋 Спринт 4 - ЗАПЛАНИРОВАН
- Система уведомлений
- Интеграция уведомлений в процессы
- Расширенная аналитика

## Модели данных

### CustomUser
- `email` - уникальный email (используется для входа)
- `first_name`, `last_name` - ФИО
- `position` - должность (Backend/Frontend/PM/Design)
- `department` - подразделение (IT/Other)
- `is_staff` - признак администратора
- `is_superuser` - признак суперадмина

### News
- `title` - заголовок новости
- `short_description` - краткое описание для карточки
- `full_text` - полный текст
- `image` - изображение
- `is_active` - активна ли новость
- `order` - порядок отображения

### Employee
- `photo` - фотография сотрудника
- `full_name` - ФИО
- `position` - должность
- `department` - подразделение
- `contact` - контакт (до 30 символов)
- `order` - порядок в слайдере

### WelcomeBlock
- `title` - заголовок приветствия
- `text` - текст приветствия
- `is_active` - активен ли блок

### Feedback
- `feedback_type` - тип (жалоба/предложение/отзыв)
- `is_anonymous` - анонимное ли обращение
- `full_name` - ФИО (для неанонимных)
- `contact_type` - тип контакта (Telegram/WhatsApp)
- `contact_value` - значение контакта
- `message` - текст обращения
- `status` - статус (новое/в обработке/решено)
- `admin_comment` - комментарий администратора

## Авторизация JWT

### Получение токенов
```bash
POST /api/v1/account/login/
{
  "email": "user@example.com",
  "password": "password"
}
```

**Ответ:**
```json
{
  "refresh": "...",
  "access": "...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "intern",
    "first_name": "Иван",
    "last_name": "Иванов"
  }
}
```

### Использование токена
Добавьте заголовок в каждый запрос:
```
Authorization: Bearer <access_token>
```

или в Swagger:
```
Authorization: JWT <access_token>
```

## Тестирование API

### Через Swagger UI
1. Откройте http://127.0.0.1:8000/api/v1/docs/
2. Нажмите "Authorize" справа вверху
3. Введите: `Bearer <ваш_access_token>`
4. Тестируйте эндпоинты

### Через Postman/Insomnia
1. Импортируйте OpenAPI схему: http://127.0.0.1:8000/api/v1/docs/?format=openapi
2. Настройте авторизацию Bearer Token
3. Выполняйте запросы

## Разработка

### Создание новой миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание нового приложения
```bash
python manage.py startapp app_name
```
Не забудьте добавить в `INSTALLED_APPS`!

### Сбор статики
```bash
python manage.py collectstatic
```

## Поддержка и контакты

Для вопросов по проекту обращайтесь к команде разработки.

---

**Статус проекта:** В активной разработке
**Версия:** 0.1.0 (Спринт 1 завершён)
# Onboarding Platform "В плюсе" - Backend API

## Описание проекта

Backend API для корпоративной onboarding-платформы компании "В плюсе". Платформа предназначена для автоматизации процесса адаптации стажёров, централизации регламентов и снижения управленческой нагрузки.

## Технологический стек

- **Python 3.x**
- **Django 5.2.11**
- **Django REST Framework**
- **PostgreSQL**
- **JWT авторизация** (djangorestframework-simplejwt)
- **Swagger/OpenAPI** (drf-yasg)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd onboarding
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
```

### 3. Активация виртуального окружения

**Windows (cmd.exe):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 6. Применение миграций
```bash
python manage.py migrate
```

### 7. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 8. Запуск сервера
```bash
python manage.py runserver 8000
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## Доступы

### Swagger документация
- **URL:** http://127.0.0.1:8000/api/v1/docs/
- Интерактивная документация всех API эндпоинтов

### Django Admin панель
- **URL:** http://127.0.0.1:8000/admin/
- Управление контентом и пользователями

## Текущие API эндпоинты

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/v1/account/login/` | Вход (получение JWT токенов) |
| POST | `/api/v1/account/logout/` | Выход (blacklist refresh token) |

### Пользователи

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/account/me/` | Текущий пользователь | Авторизованные |
| GET/PUT | `/api/v1/account/my_profile/` | Мой профиль | Авторизованные |
| POST | `/api/v1/account/admin/create/` | Создать админа | Суперадмин |
| GET | `/api/v1/account/admin/list/` | Список админов | Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/admin/{id}/` | Управление админом | Суперадмин |
| POST | `/api/v1/account/intern/create/` | Создать стажёра | Админ/Суперадмин |
| GET | `/api/v1/account/intern/list/` | Список стажёров | Админ/Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/intern/{id}/` | Управление стажёром | Админ/Суперадмин |
| GET | `/api/v1/account/superadmin/users/` | Все пользователи | Суперадмин |
| PUT | `/api/v1/account/superadmin/users/{id}/` | Изменить роль | Суперадмин |

### Главная страница

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/news/` | Список новостей (слайдер) | Авторизованные |
| GET | `/api/v1/news/{id}/` | Детали новости (лайтбокс) | Авторизованные |
| GET | `/api/v1/employees/` | Сотрудники (слайдер) | Авторизованные |
| GET | `/api/v1/welcome/` | Приветственный блок | Авторизованные |

### Обратная связь

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/v1/feedback/` | Отправить обратную связь | Авторизованные |
| GET | `/api/v1/feedback/` | Список обращений | Админ/Суперадмин |
| GET | `/api/v1/feedback/{id}/` | Детали обращения | Админ/Суперадмин |
| PATCH | `/api/v1/feedback/{id}/` | Обновить статус | Админ/Суперадмин |

## Роли пользователей

### 1. Стажёр (intern)
- `is_staff=False`, `is_superuser=False`
- Доступ к обучающим материалам и регламентам
- Может просматривать свой профиль и обновлять данные
- Может отправлять обратную связь

### 2. Администратор (admin)
- `is_staff=True`, `is_superuser=False`
- Управление контентом платформы
- Создание и управление стажёрами
- Проверка отчётов стажёров
- Просмотр обратной связи

### 3. Суперадминистратор (superadmin)
- `is_staff=True`, `is_superuser=True`
- Полный доступ ко всем функциям
- Управление администраторами
- Изменение ролей пользователей
- Системные настройки

## Структура проекта

```
onboarding/
├── account/              # Пользователи и авторизация
│   ├── migrations/
│   ├── serializers/
│   ├── views/
│   ├── models.py
│   ├── permission.py
│   └── urls.py
├── news/                 # Новости, сотрудники, приветствие
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── feedback/             # Обратная связь
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── onboard/              # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                # Загруженные файлы
├── static/               # Статические файлы
├── .env                  # Переменные окружения (не в Git!)
├── .gitignore
├── requirements.txt
├── manage.py
├── DEVELOPMENT_PLAN.md   # План развития проекта
└── README.md             # Этот файл
```

## План развития (Roadmap)

См. подробный план в файле `DEVELOPMENT_PLAN.md`

### ✅ Спринт 1 - ВЫПОЛНЕН
- Базовая авторизация и управление пользователями
- Модели для главной страницы (новости, сотрудники, приветствие)
- API для обратной связи

### ✅ Спринт 2 - ВЫПОЛНЕН
- Модели онбординга (дни, материалы, отчёты)
- API для прохождения онбординга
- Система проверки отчётов
- Статусы и валидация
- История изменений

### 📋 Спринт 3 - ЗАПЛАНИРОВАН
- Регламенты и инструкции
- График работы и календарь
- Управление через админ-панель

### 📋 Спринт 4 - ЗАПЛАНИРОВАН
- Система уведомлений
- Интеграция уведомлений в процессы
- Расширенная аналитика

## Модели данных

### CustomUser
- `email` - уникальный email (используется для входа)
- `first_name`, `last_name` - ФИО
- `position` - должность (Backend/Frontend/PM/Design)
- `department` - подразделение (IT/Other)
- `is_staff` - признак администратора
- `is_superuser` - признак суперадмина

### News
- `title` - заголовок новости
- `short_description` - краткое описание для карточки
- `full_text` - полный текст
- `image` - изображение
- `is_active` - активна ли новость
- `order` - порядок отображения

### Employee
- `photo` - фотография сотрудника
- `full_name` - ФИО
- `position` - должность
- `department` - подразделение
- `contact` - контакт (до 30 символов)
- `order` - порядок в слайдере

### WelcomeBlock
- `title` - заголовок приветствия
- `text` - текст приветствия
- `is_active` - активен ли блок

### Feedback
- `feedback_type` - тип (жалоба/предложение/отзыв)
- `is_anonymous` - анонимное ли обращение
- `full_name` - ФИО (для неанонимных)
- `contact_type` - тип контакта (Telegram/WhatsApp)
- `contact_value` - значение контакта
- `message` - текст обращения
- `status` - статус (новое/в обработке/решено)
- `admin_comment` - комментарий администратора

## Авторизация JWT

### Получение токенов
```bash
POST /api/v1/account/login/
{
  "email": "user@example.com",
  "password": "password"
}
```

**Ответ:**
```json
{
  "refresh": "...",
  "access": "...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "intern",
    "first_name": "Иван",
    "last_name": "Иванов"
  }
}
```

### Использование токена
Добавьте заголовок в каждый запрос:
```
Authorization: Bearer <access_token>
```

или в Swagger:
```
Authorization: JWT <access_token>
```

## Тестирование API

### Через Swagger UI
1. Откройте http://127.0.0.1:8000/api/v1/docs/
2. Нажмите "Authorize" справа вверху
3. Введите: `Bearer <ваш_access_token>`
4. Тестируйте эндпоинты

### Через Postman/Insomnia
1. Импортируйте OpenAPI схему: http://127.0.0.1:8000/api/v1/docs/?format=openapi
2. Настройте авторизацию Bearer Token
3. Выполняйте запросы

## Разработка

### Создание новой миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание нового приложения
```bash
python manage.py startapp app_name
```
Не забудьте добавить в `INSTALLED_APPS`!

### Сбор статики
```bash
python manage.py collectstatic
```

## Поддержка и контакты

Для вопросов по проекту обращайтесь к команде разработки.

---

**Статус проекта:** В активной разработке
**Версия:** 0.1.0 (Спринт 1 завершён)
# Onboarding Platform "В плюсе" - Backend API

## Описание проекта

Backend API для корпоративной onboarding-платформы компании "В плюсе". Платформа предназначена для автоматизации процесса адаптации стажёров, централизации регламентов и снижения управленческой нагрузки.

## Технологический стек

- **Python 3.x**
- **Django 5.2.11**
- **Django REST Framework**
- **PostgreSQL**
- **JWT авторизация** (djangorestframework-simplejwt)
- **Swagger/OpenAPI** (drf-yasg)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd onboarding
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
```

### 3. Активация виртуального окружения

**Windows (cmd.exe):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 6. Применение миграций
```bash
python manage.py migrate
```

### 7. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 8. Запуск сервера
```bash
python manage.py runserver 8000
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## Доступы

### Swagger документация
- **URL:** http://127.0.0.1:8000/api/v1/docs/
- Интерактивная документация всех API эндпоинтов

### Django Admin панель
- **URL:** http://127.0.0.1:8000/admin/
- Управление контентом и пользователями

## Текущие API эндпоинты

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/v1/account/login/` | Вход (получение JWT токенов) |
| POST | `/api/v1/account/logout/` | Выход (blacklist refresh token) |

### Пользователи

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/account/me/` | Текущий пользователь | Авторизованные |
| GET/PUT | `/api/v1/account/my_profile/` | Мой профиль | Авторизованные |
| POST | `/api/v1/account/admin/create/` | Создать админа | Суперадмин |
| GET | `/api/v1/account/admin/list/` | Список админов | Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/admin/{id}/` | Управление админом | Суперадмин |
| POST | `/api/v1/account/intern/create/` | Создать стажёра | Админ/Суперадмин |
| GET | `/api/v1/account/intern/list/` | Список стажёров | Админ/Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/intern/{id}/` | Управление стажёром | Админ/Суперадмин |
| GET | `/api/v1/account/superadmin/users/` | Все пользователи | Суперадмин |
| PUT | `/api/v1/account/superadmin/users/{id}/` | Изменить роль | Суперадмин |

### Главная страница

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/news/` | Список новостей (слайдер) | Авторизованные |
| GET | `/api/v1/news/{id}/` | Детали новости (лайтбокс) | Авторизованные |
| GET | `/api/v1/employees/` | Сотрудники (слайдер) | Авторизованные |
| GET | `/api/v1/welcome/` | Приветственный блок | Авторизованные |

### Обратная связь

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/v1/feedback/` | Отправить обратную связь | Авторизованные |
| GET | `/api/v1/feedback/` | Список обращений | Админ/Суперадмин |
| GET | `/api/v1/feedback/{id}/` | Детали обращения | Админ/Суперадмин |
| PATCH | `/api/v1/feedback/{id}/` | Обновить статус | Админ/Суперадмин |

## Роли пользователей

### 1. Стажёр (intern)
- `is_staff=False`, `is_superuser=False`
- Доступ к обучающим материалам и регламентам
- Может просматривать свой профиль и обновлять данные
- Может отправлять обратную связь

### 2. Администратор (admin)
- `is_staff=True`, `is_superuser=False`
- Управление контентом платформы
- Создание и управление стажёрами
- Проверка отчётов стажёров
- Просмотр обратной связи

### 3. Суперадминистратор (superadmin)
- `is_staff=True`, `is_superuser=True`
- Полный доступ ко всем функциям
- Управление администраторами
- Изменение ролей пользователей
- Системные настройки

## Структура проекта

```
onboarding/
├── account/              # Пользователи и авторизация
│   ├── migrations/
│   ├── serializers/
│   ├── views/
│   ├── models.py
│   ├── permission.py
│   └── urls.py
├── news/                 # Новости, сотрудники, приветствие
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── feedback/             # Обратная связь
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── onboard/              # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                # Загруженные файлы
├── static/               # Статические файлы
├── .env                  # Переменные окружения (не в Git!)
├── .gitignore
├── requirements.txt
├── manage.py
├── DEVELOPMENT_PLAN.md   # План развития проекта
└── README.md             # Этот файл
```

## План развития (Roadmap)

См. подробный план в файле `DEVELOPMENT_PLAN.md`

### ✅ Спринт 1 - ВЫПОЛНЕН
- Базовая авторизация и управление пользователями
- Модели для главной страницы (новости, сотрудники, приветствие)
- API для обратной связи

### 🔄 Спринт 2 - В РАЗРАБОТКЕ
- Модели онбординга (дни, материалы, отчёты)
- API для прохождения онбординга
- Система проверки отчётов

### 📋 Спринт 3 - ЗАПЛАНИРОВАН
- Регламенты и инструкции
- График работы и календарь
- Управление через админ-панель

### 📋 Спринт 4 - ЗАПЛАНИРОВАН
- Система уведомлений
- Интеграция уведомлений в процессы
- Расширенная аналитика

## Модели данных

### CustomUser
- `email` - уникальный email (используется для входа)
- `first_name`, `last_name` - ФИО
- `position` - должность (Backend/Frontend/PM/Design)
- `department` - подразделение (IT/Other)
- `is_staff` - признак администратора
- `is_superuser` - признак суперадмина

### News
- `title` - заголовок новости
- `short_description` - краткое описание для карточки
- `full_text` - полный текст
- `image` - изображение
- `is_active` - активна ли новость
- `order` - порядок отображения

### Employee
- `photo` - фотография сотрудника
- `full_name` - ФИО
- `position` - должность
- `department` - подразделение
- `contact` - контакт (до 30 символов)
- `order` - порядок в слайдере

### WelcomeBlock
- `title` - заголовок приветствия
- `text` - текст приветствия
- `is_active` - активен ли блок

### Feedback
- `feedback_type` - тип (жалоба/предложение/отзыв)
- `is_anonymous` - анонимное ли обращение
- `full_name` - ФИО (для неанонимных)
- `contact_type` - тип контакта (Telegram/WhatsApp)
- `contact_value` - значение контакта
- `message` - текст обращения
- `status` - статус (новое/в обработке/решено)
- `admin_comment` - комментарий администратора

### OnboardingDay
- `day_number` - номер дня (уникальный)
- `title` - название дня
- `description` - описание целей дня
- `instructions` - текстовые инструкции
- `deadline_time` - дедлайн сдачи отчёта (ЧЧ:ММ)
- `is_active` - активен ли день
- `order` - порядок отображения

### OnboardingMedia
- `onboarding_day` - привязка к дню
- `media_type` - тип (ссылка/видео/изображение/файл)
- `title` - название материала
- `link` - ссылка (для типов: ссылка, видео)
- `file` - файл (для типов: изображение, файл)
- `order` - порядок отображения

### DailyReport
- `intern` - стажёр (FK)
- `onboarding_day` - день онбординга (FK)
- `what_done` - что сделал
- `what_will_do` - что буду делать
- `problems` - какие проблемы возникли
- `attachment_link` - ссылка на результат
- `attachment_file` - файл с результатом
- `status` - статус (черновик/отправлен/принят/на доработку/отклонён)
- `submitted_at` - дата отправки
- `reviewer` - проверяющий (FK)
- `reviewer_comment` - комментарий проверяющего
- `reviewed_at` - дата проверки

## Авторизация JWT

### Получение токенов
```bash
POST /api/v1/account/login/
{
  "email": "user@example.com",
  "password": "password"
}
```

**Ответ:**
```json
{
  "refresh": "...",
  "access": "...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "intern",
    "first_name": "Иван",
    "last_name": "Иванов"
  }
}
```

### Использование токена
Добавьте заголовок в каждый запрос:
```
Authorization: Bearer <access_token>
```

или в Swagger:
```
Authorization: JWT <access_token>
```

## Тестирование API

### Через Swagger UI
1. Откройте http://127.0.0.1:8000/api/v1/docs/
2. Нажмите "Authorize" справа вверху
3. Введите: `Bearer <ваш_access_token>`
4. Тестируйте эндпоинты

### Через Postman/Insomnia
1. Импортируйте OpenAPI схему: http://127.0.0.1:8000/api/v1/docs/?format=openapi
2. Настройте авторизацию Bearer Token
3. Выполняйте запросы

## Разработка

### Создание новой миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание нового приложения
```bash
python manage.py startapp app_name
```
Не забудьте добавить в `INSTALLED_APPS`!

### Сбор статики
```bash
python manage.py collectstatic
```

## Поддержка и контакты

Для вопросов по проекту обращайтесь к команде разработки.

---

**Статус проекта:** В активной разработке
**Версия:** 0.1.0 (Спринт 1 завершён)
# Onboarding Platform "В плюсе" - Backend API

## Описание проекта

Backend API для корпоративной onboarding-платформы компании "В плюсе". Платформа предназначена для автоматизации процесса адаптации стажёров, централизации регламентов и снижения управленческой нагрузки.

## Технологический стек

- **Python 3.x**
- **Django 5.2.11**
- **Django REST Framework**
- **PostgreSQL**
- **JWT авторизация** (djangorestframework-simplejwt)
- **Swagger/OpenAPI** (drf-yasg)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd onboarding
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
```

### 3. Активация виртуального окружения

**Windows (cmd.exe):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 6. Применение миграций
```bash
python manage.py migrate
```

### 7. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 8. Запуск сервера
```bash
python manage.py runserver 8000
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## Доступы

### Swagger документация
- **URL:** http://127.0.0.1:8000/api/v1/docs/
- Интерактивная документация всех API эндпоинтов

### Django Admin панель
- **URL:** http://127.0.0.1:8000/admin/
- Управление контентом и пользователями

## Текущие API эндпоинты

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/v1/account/login/` | Вход (получение JWT токенов) |
| POST | `/api/v1/account/logout/` | Выход (blacklist refresh token) |

### Пользователи

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/account/me/` | Текущий пользователь | Авторизованные |
| GET/PUT | `/api/v1/account/my_profile/` | Мой профиль | Авторизованные |
| POST | `/api/v1/account/admin/create/` | Создать админа | Суперадмин |
| GET | `/api/v1/account/admin/list/` | Список админов | Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/admin/{id}/` | Управление админом | Суперадмин |
| POST | `/api/v1/account/intern/create/` | Создать стажёра | Админ/Суперадмин |
| GET | `/api/v1/account/intern/list/` | Список стажёров | Админ/Суперадмин |
| GET/PUT/DELETE | `/api/v1/account/intern/{id}/` | Управление стажёром | Админ/Суперадмин |
| GET | `/api/v1/account/superadmin/users/` | Все пользователи | Суперадмин |
| PUT | `/api/v1/account/superadmin/users/{id}/` | Изменить роль | Суперадмин |

### Главная страница

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/news/` | Список новостей (слайдер) | Авторизованные |
| GET | `/api/v1/news/{id}/` | Детали новости (лайтбокс) | Авторизованные |
| GET | `/api/v1/employees/` | Сотрудники (слайдер) | Авторизованные |
| GET | `/api/v1/welcome/` | Приветственный блок | Авторизованные |

### Обратная связь

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/v1/feedback/` | Отправить обратную связь | Авторизованные |
| GET | `/api/v1/feedback/` | Список обращений | Админ/Суперадмин |
| GET | `/api/v1/feedback/{id}/` | Детали обращения | Админ/Суперадмин |
| PATCH | `/api/v1/feedback/{id}/` | Обновить статус | Админ/Суперадмин |

### Онбординг и отчёты

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/onboarding/days/` | Список дней онбординга | Авторизованные |
| GET | `/api/v1/onboarding/days/{id}/` | Детали дня + материалы | Авторизованные |
| GET | `/api/v1/reports/my/` | Мои отчёты | Стажёр |
| GET | `/api/v1/reports/all/` | Все отчёты (с фильтрами) | Админ/Суперадмин |
| POST | `/api/v1/reports/` | Создать отчёт | Стажёр |
| PUT/PATCH | `/api/v1/reports/{id}/` | Обновить черновик | Стажёр |
| POST | `/api/v1/reports/{id}/submit/` | Отправить на проверку | Стажёр |
| PATCH | `/api/v1/reports/{id}/review/` | Проверить отчёт | Админ/Суперадмин |
| GET | `/api/v1/reports/{id}/history/` | История отчёта | Авторизованные |

### Регламенты

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/regulations/` | Список регламентов | Авторизованные |
| GET | `/api/v1/regulations/{id}/` | Детали регламента | Авторизованные |

### График работы

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/schedule/types/` | Типы графиков | Авторизованные |
| GET | `/api/v1/schedule/my/` | Мой график | Авторизованные |
| PUT | `/api/v1/schedule/my/` | Выбрать график | Авторизованные |
| GET | `/api/v1/schedule/holidays/` | Праздники | Авторизованные |
| GET | `/api/v1/schedule/calendar/` | Календарь месяца | Авторизованные |

### Инструкции

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/instructions/` | Инструкция платформы | Авторизованные |

## Роли пользователей

### 1. Стажёр (intern)
- `is_staff=False`, `is_superuser=False`
- Доступ к обучающим материалам и регламентам
- Может просматривать свой профиль и обновлять данные
- Может отправлять обратную связь

### 2. Администратор (admin)
- `is_staff=True`, `is_superuser=False`
- Управление контентом платформы
- Создание и управление стажёрами
- Проверка отчётов стажёров
- Просмотр обратной связи

### 3. Суперадминистратор (superadmin)
- `is_staff=True`, `is_superuser=True`
- Полный доступ ко всем функциям
- Управление администраторами
- Изменение ролей пользователей
- Системные настройки

## Структура проекта

```
onboarding/
├── account/              # Пользователи и авторизация
│   ├── migrations/
│   ├── serializers/
│   ├── views/
│   ├── models.py
│   ├── permission.py
│   └── urls.py
├── news/                 # Новости, сотрудники, приветствие
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── feedback/             # Обратная связь
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── onboard/              # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                # Загруженные файлы
├── static/               # Статические файлы
├── .env                  # Переменные окружения (не в Git!)
├── .gitignore
├── requirements.txt
├── manage.py
├── DEVELOPMENT_PLAN.md   # План развития проекта
└── README.md             # Этот файл
```

## План развития (Roadmap)

См. подробный план в файле `DEVELOPMENT_PLAN.md`

### ✅ Спринт 1 - ВЫПОЛНЕН
- Базовая авторизация и управление пользователями
- Модели для главной страницы (новости, сотрудники, приветствие)
- API для обратной связи

### 🔄 Спринт 2 - В РАЗРАБОТКЕ
- Модели онбординга (дни, материалы, отчёты)
- API для прохождения онбординга
- Система проверки отчётов

### 📋 Спринт 3 - ЗАПЛАНИРОВАН
- Регламенты и инструкции
- График работы и календарь
- Управление через админ-панель

### 📋 Спринт 4 - ЗАПЛАНИРОВАН
- Система уведомлений
- Интеграция уведомлений в процессы
- Расширенная аналитика

## Модели данных

### CustomUser
- `email` - уникальный email (используется для входа)
- `first_name`, `last_name` - ФИО
- `position` - должность (Backend/Frontend/PM/Design)
- `department` - подразделение (IT/Other)
- `is_staff` - признак администратора
- `is_superuser` - признак суперадмина

### News
- `title` - заголовок новости
- `short_description` - краткое описание для карточки
- `full_text` - полный текст
- `image` - изображение
- `is_active` - активна ли новость
- `order` - порядок отображения

### Employee
- `photo` - фотография сотрудника
- `full_name` - ФИО
- `position` - должность
- `department` - подразделение
- `contact` - контакт (до 30 символов)
- `order` - порядок в слайдере

### WelcomeBlock
- `title` - заголовок приветствия
- `text` - текст приветствия
- `is_active` - активен ли блок

### Feedback
- `feedback_type` - тип (жалоба/предложение/отзыв)
- `is_anonymous` - анонимное ли обращение
- `full_name` - ФИО (для неанонимных)
- `contact_type` - тип контакта (Telegram/WhatsApp)
- `contact_value` - значение контакта
- `message` - текст обращения
- `status` - статус (новое/в обработке/решено)
- `admin_comment` - комментарий администратора

## Авторизация JWT

### Получение токенов
```bash
POST /api/v1/account/login/
{
  "email": "user@example.com",
  "password": "password"
}
```

**Ответ:**
```json
{
  "refresh": "...",
  "access": "...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "intern",
    "first_name": "Иван",
    "last_name": "Иванов"
  }
}
```

### Использование токена
Добавьте заголовок в каждый запрос:
```
Authorization: Bearer <access_token>
```

или в Swagger:
```
Authorization: JWT <access_token>
```

## Тестирование API

### Через Swagger UI
1. Откройте http://127.0.0.1:8000/api/v1/docs/
2. Нажмите "Authorize" справа вверху
3. Введите: `Bearer <ваш_access_token>`
4. Тестируйте эндпоинты

### Через Postman/Insomnia
1. Импортируйте OpenAPI схему: http://127.0.0.1:8000/api/v1/docs/?format=openapi
2. Настройте авторизацию Bearer Token
3. Выполняйте запросы

## Разработка

### Создание новой миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание нового приложения
```bash
python manage.py startapp app_name
```
Не забудьте добавить в `INSTALLED_APPS`!

### Сбор статики
```bash
python manage.py collectstatic
```

## Поддержка и контакты

Для вопросов по проекту обращайтесь к команде разработки.

---

**Статус проекта:** В активной разработке
**Версия:** 0.1.0 (Спринт 1 завершён)

