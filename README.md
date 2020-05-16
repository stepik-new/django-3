# Учебный проект по Django

## Перед запуском сервера

Установите необходимые зависимости (Python 3.7):

    > pip install requirements.txt

Выполните команды для настройки БД:

    > python manage.py makemigrations vacancies
    > python manage.py migrate vacancies
    
Загрузите демо-данные в БД:

- Перейдите в shell

        > python manage.py shell
- Выполните импорт скрипта

        > import update_db
        
## Запуск сервера

Для запуска сервера выполните команду:

    > python manage.py runserver
