from telebot.types import Message
from internal.gpt import gpt4, bard
from internal.csv import elections
from internal import utils
import telebot
import os

from io import BytesIO
import pandas as pd

print("Setup telegram bot ")



# Замените 'YOUR_BOT_TOKEN' на ваш API токен Telegram бота
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
ADMINS = ["kirillyat"]


@bot.message_handler(commands=["ping"])
def handle_ping_message(message: Message):
    print(f"Handle request from {message.from_user.username}")
    print(f"Content {message.text}")
    if message.from_user.username in ADMINS and "-m" in message.text:
        bot.reply_to(message, str(message))

    bot.reply_to(message, "pong")


@bot.message_handler(commands=["gpt4"])
def handle_gpt4_message(message: Message):
    print(f"Handle request from {message.from_user.username}")
    print(f"Content {message.text}")
    try:
        answer = gpt4(message.text)
        bot.reply_to(message, answer)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Failed to request. \nTry one more time.")

@bot.message_handler(commands=["bard"])
def handle_bard_message(message: Message):
    print(f"Handle request from {message.from_user.username}")
    print(f"Content {message.text}")
    try:
        answer = bard(message.text)
        bot.reply_to(message, answer)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Failed to request. \nTry one more time.")


@bot.message_handler(commands=["upper"])
def handle_upper_message(message: Message):
    print(f"Handle request from {message.from_user.username}")
    print(f"Content {message.text}")

    bot.reply_to(message, message.text.upper())

@bot.message_handler(commands=["lower"])
def handle_lower_message(message: Message):
    print(f"Handle request from {message.from_user.username}")
    print(f"Content {message.text}")

    bot.reply_to(message, message.text.lower())


# Обработчик загрузки документа
@bot.message_handler(content_types=['document'])
def handle_document(message: Message):


    if message.document.mime_type == 'text/csv':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name, _ = utils.file_name_type(message.document.file_name)
        # Чтение CSV-файла и преобразование в формат Excel
        responce = elections(BytesIO(downloaded_file))
        responce.name = name+'.xlsx'
        
        # Отправка файла Excel обратно пользователю
        bot.send_document(message.chat.id, document=responce)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте CSV-файл.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
