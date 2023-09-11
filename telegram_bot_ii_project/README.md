# Выполнение технического задания MindFusion

Стек технологий, используемых в проекте:

- **Django**: Для управления базой данных.
- **Amplitude**: Для отправки уведомлений.
- **python-telegram-bot**: Для разработки Telegram бота.
- **API chat GPT**: Для взаимодействия с искусственным интеллектом.

## Источники

- [Ссылка на Miro](https://miro.com/welcomeonboard/Sm9ncTNtdjZMbXNIbWlqb0E4Q2dneUh0UFdUd0lrQ1RCcmZ3TExKRkpwYng3ejdVelduZ0NEQkVKUlliZnozVnwzNDU4NzY0NTU2NDgxNjUxODI1fDI=?share_link_id=462901074834)
- [Ссылка на Adobe XD](https://xd.adobe.com/view/58fface2-d5a1-4572-af02-5fac362d3fa4-0dac/)

## Запуск бота

Для запуска бота выполните следующие шаги:

1. Перейдите в директорию проекта:

   ```bash
   cd telegram_bot_ii_project

2.  Установка зависимостей:

   ```bash
   pip install -r requirements.txt

3. Создайте суперпользователя для Django:

   ```bash
   python manage.py createsuperuser

4. Примените миграции для базы данных:

   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. Запустите бота:

   ```bash
   python manage.py bot

## Контакты
- **Амир Гараев**
- **amir.66garaev@gmail.com**
- **https://t.me/de_la_verrier**