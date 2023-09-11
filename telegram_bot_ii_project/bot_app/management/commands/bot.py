from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from bot_app.models import UserProfile,Character,DialogMessage
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

        api_key = '810784fe2ce79942706d47d9c83614fc'
        endpoint = 'https://api2.amplitude.com/2/httpapi'
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

        # Отправляем событие получение ответа от API в Amplitude
        def send_amplitude_message_received(success: bool, user_id: str):
            event_data = {
                'api_key': api_key,
                'events': [{
                    'user_id': user_id,
                    'event_type': 'MessageReceived',
                    'user_properties': {
                        'is_successful': success
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

            message_text = f"Привет, {user.first_name}! Я - ваш бот. Я могу сделать много полезных вещей."


            button_text = "Перейти в Telegram Web App"
            web_app_url = "https://web.telegram.org"
            button_url = f"{web_app_url}/"
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=button_url)]])

            #приветственное сообщение кнопкой
            update.message.reply_text(message_text, reply_markup=keyboard)

            #событие регистрации в Amplitude
            current_time = timezone.now()
            send_amplitude_event(user.id, user.username, user.first_name, user.last_name, current_time)

            #запись UserProfile в базе данных
            user_profile, created = UserProfile.objects.get_or_create(
                chat_id=user.id,
                defaults={
                    'user_name': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'time': current_time
                }
            )

            if created:
                print("User profile created:", user_profile)
            else:
                print("User profile already exists:", user_profile)


        def menu(update: Update, context: CallbackContext):
            user = update.effective_user

            #событие "Открыто меню" в Amplitude
            send_amplitude_event(user.id, user.username, user.first_name, user.last_name,
                                 datetime.now())


            menu_text = "Выберите опцию из меню:"


            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Марио", callback_data="mario"),
                    InlineKeyboardButton("Альберт Энштейн", callback_data="einstein"),
                ]
            ])

            #сообщение с клавиатурой
            update.message.reply_text(menu_text, reply_markup=keyboard)

        def menu_choice(update: Update, context: CallbackContext):
            query = update.callback_query
            user = update.effective_user
            data = query.data

            if data == "mario":
                send_amplitude_event(user.id, user.username, user.first_name, user.last_name, timezone.now())

                mario = Character.objects.get(name="Марио")

                #запись UserProfile с выбором Марио
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

                print('menu_choice')
                print("User chose Mario")
                print(f"Current state: {context.user_data['state']}")

                return MARO_STATE

            elif data == "einstein":
                send_amplitude_event(user.id, user.username, user.first_name, user.last_name, timezone.now())


                einstein = Character.objects.get(name="Альберт Энштейн")

                #запись UserProfile с выбором Альберта Энштейна
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

                print('menu_choice')
                print("User chose Einstein")
                print(f"State: {context.user_data['state']}")

                return EINSTEIN_STATE

        def send_message_to_chatgpt(messages):
            chatgpt_server_url = 'http://95.217.14.178:8080/candidates_openai/gpt'

            data = {
                'model': 'gpt-3.5-turbo',
                'messages': messages,
            }

            response = requests.post(chatgpt_server_url, json=data)

            if response.status_code == 200:
                return response.json()
            else:
                return None

        def receive_question(update: Update, context: CallbackContext):
            user_input = update.message.text
            state = context.user_data.get('state')
            print(f"receive_question")
            print(f"State: {state}")

            prompt = context.user_data.get('prompt', "")
            print(f"Prompt: {prompt}")

            chatgpt_input = f"{context.user_data['character']}: {user_input}"
            messages = [
                {"role": "system", "content": context.user_data['prompt']},
                {"role": "user", "content": chatgpt_input},
            ]

            #сообщения в ChatGPT и получаем ответ
            response = send_message_to_chatgpt(messages)

            if response and response['choices'][0]['message']['content']:
                # Извлекаем текст ответа от ChatGPT
                chatgpt_response = response['choices'][0]['message']['content']

                # Сохраняем сообщение пользователя в модели DialogMessage
                user_id = update.effective_user.id
                character_name = context.user_data['character']
                message_text = user_input
                dialog_message = DialogMessage(user_id=user_id, character_name=character_name,
                                               message_text=message_text)
                dialog_message.save()

                send_amplitude_message_received(True,user_id)

                # Отправляем ответ пользователю
                update.message.reply_text(chatgpt_response)
            else:
                # Сохраняем сообщение пользователя в модели DialogMessage
                user_id = update.effective_user.id
                character_name = context.user_data['character']
                message_text = user_input
                dialog_message = DialogMessage(user_id=user_id, character_name=character_name,
                                               message_text=message_text)
                dialog_message.save()

                send_amplitude_message_received(False, user_id)
                update.message.reply_text(
                    "Извините, произошла ошибка при получении ответа от ChatGPT или ответ пустой.")


        updater = Updater(token=bot_token, use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("menu", menu))
        dispatcher.add_handler(CallbackQueryHandler(menu_choice))
        receive_question_handler = MessageHandler(Filters.text & ~Filters.command, receive_question)
        dispatcher.add_handler(receive_question_handler)


        updater.start_polling()
        updater.idle()