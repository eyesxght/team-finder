# TeamFinder

Платформа для поиска команды на Pet-проекты. Разработчики, дизайнеры и другие специалисты могут публиковать идеи проектов, находить единомышленников и откликаться на опубликованные предложения.

## Функциональность

- Регистрация и аутентификация по email
- Публикация, редактирование и завершение проектов
- Вступление/выход из проекта
- Добавление проектов в избранное
- Фильтрация пользователей по критериям (авторы избранных, соучастники и др.)
- Личный профиль: аватар, контакты, GitHub, описание
- Постраничная пагинация (12 элементов на страницу)
- Автогенерация аватара при регистрации

## Стек технологий

| Компонент       | Технология                          |
|-----------------|-------------------------------------|
| Backend         | Python 3.11+, Django 5.x            |
| База данных     | PostgreSQL (запуск через Docker)    |
| Аутентификация  | Кастомный `AbstractBaseUser`        |
| Изображения     | Pillow (генерация аватаров)         |
| Конфигурация    | python-decouple (`.env`)            |
| Контейнер БД    | Docker Compose                      |

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/eyesxght/team-finder-ad-main.git
cd team-finder-ad-main
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (cmd):**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать файл `.env`

Скопируйте пример и заполните своими значениями:

```bash
cp .env_example .env
```

| Переменная              | Описание                                                                                           | Пример                        |
|-------------------------|----------------------------------------------------------------------------------------------------|-------------------------------|
| `DJANGO_SECRET_KEY`     | Секретный ключ Django. Сгенерировать: `from django.core.management.utils import get_random_secret_key; get_random_secret_key()` | `your-secret-key`            |
| `DJANGO_DEBUG`          | Режим отладки (`True` при разработке, `False` в продакшне)                                         | `True`                        |
| `DJANGO_ALLOWED_HOSTS`  | Список допустимых хостов через запятую                                                             | `localhost,127.0.0.1`         |
| `POSTGRES_DB`           | Имя базы данных PostgreSQL                                                                         | `teamfinder`                  |
| `POSTGRES_USER`         | Пользователь PostgreSQL                                                                            | `postgres`                    |
| `POSTGRES_PASSWORD`     | Пароль PostgreSQL                                                                                  | `password`                    |
| `POSTGRES_HOST`         | Адрес сервера БД                                                                                   | `localhost`                   |
| `POSTGRES_PORT`         | Порт PostgreSQL                                                                                    | `5432`                        |

### 5. Запустить PostgreSQL через Docker

```bash
docker compose up -d
```

Остановить:
```bash
docker compose down
```

> Если на порту 5432 уже работает другой сервер БД, измените порт в `docker-compose.yml` (`"5433:5432"`) и в `.env` (`POSTGRES_PORT=5433`).

### 6. Применить миграции

```bash
python manage.py migrate
```

### 7. Запустить сервер разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

## Автор

GitHub: [@eyesxght](https://github.com/eyesxght)
