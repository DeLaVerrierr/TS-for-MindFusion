from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from bot_app.models import UserProfile,Character
import requests
import json
from telegram.ext import CommandHandler, CallbackContext
from telegram.ext import CommandHandler, CallbackContext
from django.utils import timezone
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from datetime import datetime


MARO_STATE, EINSTEIN_STATE = range(2)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Ваши настройки Amplitude

        api_key = '810784fe2ce79942706d47d9c83614fc'
        endpoint = 'https://api2.amplitude.com/2/httpapi'

        # Токен вашего бота
        bot_token = '6332428791:AAEK9x9vh7d8YpWvVtckhOdOKDUKRqtlSe8'

        # Отправляем событие регистрации в Amplitude
        def send_amplitude_event(user_id, user_name, name, surname, time):
            event_data = {
                'api_key': api_key,
                'events': [{
                    'user_id': user_id,
                    'event_type': 'Registration',
                    'user_properties': {
                        'user_name': user_name,
                        'name': name,
                        'surname': surname,
                        'time': time.isoformat()
                    }
                }]
            }

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }

            response = requests.post(endpoint, headers=headers, data=json.dumps(event_data))

            if response.status_code == 200:
                print("Success:", response.json())
            else:
                print("Error:", response.text)


        def start(update: Update, context: CallbackContext):
            user = update.effective_user

            # Текст приветственного сообщения с объяснением и прикрепленной кнопкой
            message_text = f"Привет, {user.first_name}! Я - ваш бот. Я могу сделать много полезных вещей."

            # Создаем инлайн кнопку "Перейти в Telegram Web App"
            button_text = "Перейти в Telegram Web App"
            web_app_url = "https://web.telegram.org"  # URL Telegram Web App
            button_url = f"{web_app_url}/"
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=button_url)]])

            # Отправляем приветственное сообщение с прикрепленной кнопкой
            update.message.reply_text(message_text, reply_markup=keyboard)

            # Отправляем событие регистрации в Amplitude
            current_time = timezone.now()  # Получаем текущее время с учетом часового пояса
            send_amplitude_event(user.id, user.username, user.first_name, user.last_name, current_time)

            # Создаем и сохраняем запись UserProfile в базе данных
            user_profile, created = UserProfile.objects.get_or_create(
                chat_id=user.id,
                defaults={
                    'user_name': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'time': current_time  # Используем текущее время с учетом часового пояса
                }
            )

            if created:
                print("User profile created:", user_profile)
            else:
                print("User profile already exists:", user_profile)

        # Функция для обработки команды /menu
        def menu(update: Update, context: CallbackContext):
            user = update.effective_user

            # Отправляем событие "Открыто меню" в Amplitude
            send_amplitude_event(user.id, user.username, user.first_name, user.last_name,
                                 datetime.now())  # Используем datetime.now() вместо строки

            # Текст сообщения для меню
            menu_text = "Выберите опцию из меню:"

            # Создаем инлайн клавиатуру с двумя кнопками
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Марио", callback_data="mario"),
                    InlineKeyboardButton("Альберт Энштейн", callback_data="einstein"),
                ]
            ])

            # Отправляем сообщение с клавиатурой
            update.message.reply_text(menu_text, reply_markup=keyboard)

        def menu_choice(update: Update, context: CallbackContext):
            query = update.callback_query
            user = update.effective_user
            data = query.data

            if data == "mario":
                send_amplitude_event(user.id, user.username, user.first_name, user.last_name, timezone.now())

                # Получаем информацию о Марио из базы данных
                mario = Character.objects.get(name="Марио")

                # Обновляем запись UserProfile с выбором Марио
                user_profile, _ = UserProfile.objects.get_or_create(chat_id=user.id)
                user_profile.choice = "Марио"
                user_profile.save()

                # Устанавливаем состояние и промпт для Марио
                context.user_data['character'] = 'Марио'
                context.user_data['state'] = MARO_STATE
                context.user_data[
                    'prompt'] = "Привет, я Марио! Я знаменитый герой игры, всегда готовый к новым приключениям. Мы можем поговорить о моих приключениях, играх и многом другом. Задавай свои вопросы, и я отвечу в фирменном стиле!"

                # Задаем промпт для Марио
                query.message.reply_text(
                    context.user_data['prompt'])

                # Сохраняем prompt в контексте пользователя
                context.user_data['prompt'] = context.user_data.get('prompt', "")

                # Отладочные сообщения
                print("User chose Mario")
                print(f"Current state: {context.user_data['state']}")

                return MARO_STATE

            elif data == "einstein":
                send_amplitude_event(user.id, user.username, user.first_name, user.last_name, timezone.now())

                # Получаем информацию об Альберте Энштейне из базы данных
                einstein = Character.objects.get(name="Альберт Энштейн")

                # Обновляем запись UserProfile с выбором Альберта Энштейна
                user_profile, _ = UserProfile.objects.get_or_create(chat_id=user.id)
                user_profile.choice = "Альберт Энштейн"
                user_profile.save()

                # Устанавливаем состояние и промпт для Альберта Энштейна
                context.user_data['character'] = 'Альберт Энштейн'
                context.user_data['state'] = EINSTEIN_STATE
                context.user_data[
                    'prompt'] = "Привет, я Альберт Энштейн! Я известный физик и ученый. Мы можем обсудить науку, теорию относительности и многое другое. Задавайте вопросы, и я постараюсь ответить как ученый!"

                # Задаем промпт для Альберта Энштейна
                query.message.reply_text(
                    context.user_data['prompt'])

                # Сохраняем prompt в контексте пользователя
                context.user_data['prompt'] = context.user_data.get('prompt', "")

                # Отладочные сообщения
                print("User chose Einstein")
                print(f"Current state: {context.user_data['state']}")

                return EINSTEIN_STATE

        def send_message_to_chatgpt(messages, state):
            chatgpt_server_url = 'http://95.217.14.178:8080/candidates_openai/gpt'
            prompt = ''
            # Определите промпт в зависимости от состояния
            if state == MARO_STATE:
                prompt = "Привет, я Марио! Я знаменитый герой игры, всегда готовый к новым приключениям. Мы можем поговорить о моих приключениях, играх и многом другом. Задавай свои вопросы, и я отвечу в фирменном стиле!"
            elif state == EINSTEIN_STATE:
                prompt = "Привет, я Альберт Энштейн! Я известный физик и ученый. Мы можем обсудить науку, теорию относительности и многое другое. Задавайте вопросы, и я постараюсь ответить как ученый!"

            # Выводим значения промпта и состояния для отладки
            print(f"State in send_message_to_chatgpt: {state}")
            print(f"Prompt in send_message_to_chatgpt: {prompt}")

            # Формируем JSON-запрос с сообщениями и текущим промптом
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': messages,
                'options': {'prompt': prompt},  # Используйте options для передачи prompt
            }

            # Отправляем POST-запрос к серверу ChatGPT
            response = requests.post(chatgpt_server_url, json=data)

            # Отладочный вывод
            print(f"HTTP Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")

            if response.status_code == 200:
                return response.json()
            else:
                return None

        def receive_question(update: Update, context: CallbackContext):
            user = update.effective_user
            user_input = update.message.text
            state = context.user_data.get('state')

            # Выводим значения state и prompt для отладки
            print(f"State in receive_question: {state}")
            prompt = context.user_data.get('prompt', "")
            print(f"Prompt in receive_question: {prompt}")

            if state == MARO_STATE:
                # Задаем промпт для Марио
                prompt = context.user_data.get('prompt', "")
            elif state == EINSTEIN_STATE:
                # Задаем промпт для Альберта Энштейна
                prompt = context.user_data.get('prompt', "")

            # Добавляем вопрос пользователя к промпту
            prompt += user_input

            # Формируем сообщения для отправки в ChatGPT, включая системное сообщение
            messages = [
                {"role": "system", "content": "СИСТЕМНОЕ СООБЩЕНИЕ"},
                {"role": "user", "content": user_input},
            ]

            # Отправляем сообщения в ChatGPT и получаем ответ
            response = send_message_to_chatgpt(messages, state)


            if response and response['choices'][0]['message']['content']:
                # Извлекаем текст ответа от ChatGPT
                chatgpt_response = response['choices'][0]['message']['content']

                # Отправляем ответ пользователю
                update.message.reply_text(chatgpt_response)
            else:
                # Если не удалось получить ответ от ChatGPT или ответ пустой
                update.message.reply_text(
                    "Извините, произошла ошибка при получении ответа от ChatGPT или ответ пустой.")


        # Настройки бота
        updater = Updater(token=bot_token, use_context=True)
        dispatcher = updater.dispatcher

        # Добавляем обработчик команды /start
        dispatcher.add_handler(CommandHandler("start", start))

        # Добавляем обработчик команды /menu
        dispatcher.add_handler(CommandHandler("menu", menu))

        # Добавляем обработчик выбора опции из меню
        dispatcher.add_handler(CallbackQueryHandler(menu_choice))
        receive_question_handler = MessageHandler(Filters.text & ~Filters.command, receive_question)
        dispatcher.add_handler(receive_question_handler)


        # Запускаем бота
        updater.start_polling()
        updater.idle()