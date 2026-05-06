# Image Service

Микросервис на Django для загрузки, просмотра, получения и удаления изображений.

## Возможности

- загрузка изображений
- получение изображения по id
- удаление изображения по id
- HTML-страницы для работы с изображениями
- PostgreSQL
- Docker Compose
- .env настройки
- тесты API
- отчет покрытия тестами

## Запуск проекта

1. Клонировать репозиторий:

```bash
git clone https://github.com/ТВОЙ_НИК/image-service.git
cd image-service
Создать .env файл на основе примера:
cp .env.example .env
Запустить проект через Docker Compose:
docker compose up --build
Применить миграции:
docker compose exec web python manage.py migrate
Открыть проект:

http://127.0.0.1:8000/

Запуск тестов
docker compose exec web python manage.py test
Отчет покрытия тестами
docker compose exec web coverage run --source=main manage.py test main
docker compose exec web coverage html

HTML-отчет будет создан в папке:

htmlcov/

Переменные окружения

Пример находится в файле:

.env.example

Реальный .env файл не загружается в Git.

Что не загружается в Git
.env
.venv
.idea
pycache
локальная база данных
загруженные изображения

---
