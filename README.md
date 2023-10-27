# Бэкенд для SPA веб приложения

## Описание
REST API на основе DRF для приложения по работе с атомарными привычками.
Пользователь имеет доступ к регистрации и авторизации пользователей, CRUD механизму
модели привычек. Система поддерживает разделение прав доступа, на основе JWT токенов,
валидацию на уровне сериализаторов.
Также реализована интеграция с API telegram, для рассылки уведомлений.
Проект покрыт unit тестами и задокументирован.

## Пример получаемых данных на GET запрос
![example1.png](readme_assets%2Fexample1.png)

## Описание структуры проекта
* habits
  - accounts - Приложение для работы с пользователями
  - habits - Настройки проекта
  - habits_app - Приложение для работы с привычками
  - utils - Пакет для работы для сторонней логики
    - TG.py - Файл интеграции с Telegram API
  - manage.py

* readme_assets - Файлы для README.md
* .env.sample - Образец для создания env файла
* README.md

## Инициализация проекта

**Для работы проекта требуется PostgreSQL, Redis**

  ```sh
  git clone https://github.com/Lio-Kay/DRF_Habits_Tracker
  ```

Создайте файл .env рядом с .env.sample и заполните его

Создайте БД Postgres, запустите Redis

Запустите через консоль:
  ```sh
  poetry update
  cd .\habits\
  python manage.py runserver
  ```
Для работы с telegram:
  ```sh
  unix:
  celery -A habits worker -l INFO
  windos:
  celery -A habits1 worker -l INFO -S eventlet
  ---
  celery -A habits beat -l INFO -S eventlet
  ```

## Технологии в проекте
Библиотеки:
* Django+DRF;
  - drf-yasg;
  - djangorestframework-simlejwt;
  - django-cors-headers;
* redis;
* celery;
* psycopg2-binary;
* python-dotenv;
* requests.

Другие особенности:
* Переопределены модели BaseUserManager, AbstractUser для регистрации пользователя
* Покрытие тестами более 90%
* Документация эндпоинтов на основе OpenAPI

## Возможные улучшения
* Добавить валидацию на уровне модели
* Реализовать авторизацию через allauth