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
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ADMINS = ["kirillyat"]
logging_chat = os.getenv("LOGGER_CHAT")


def info(message: Message, info: str = ""):
    text = f"""
Username: {message.from_user.username}
Chat ID: {message.chat.id}
Input: {message.text}
Logging: {info or 'Null'}
"""
    print(text)
    bot.send_message(chat_id=logging_chat, text=text)


@bot.message_handler(commands=["ping"])
def handle_ping_message(message: Message):
    info(message)
    if message.from_user.username in ADMINS and "-m" in message.text:
        bot.reply_to(message, str(message))

    bot.reply_to(message, "pong")


@bot.message_handler(commands=["gpt4", "gpt", "gpt3", "chatgpt"])
def handle_gpt4_message(message: Message):
    info(message)
    try:
        _, text = utils.comand_text(message.text)
        answer = gpt4(text)
        bot.reply_to(message, answer)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Failed to request. \nTry one more time.")


@bot.message_handler(commands=["bard"])
def handle_bard_message(message: Message):
    info(message)

    try:
        answer = bard(message.text)
        bot.reply_to(message, answer)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Failed to request. \nTry one more time.")


@bot.message_handler(commands=["upper"])
def handle_upper_message(message: Message):
    info(message)
    bot.reply_to(message, message.text.upper())

@bot.message_handler(commands=["send"])
def handle_send_message(message: Message):
    info(message)
    tokens = message.text.split()
    bot.send_message(chat_id=tokens[1], text=" ".join(tokens[2:]))

@bot.message_handler(commands=["lower"])
def handle_lower_message(message: Message):
    info(message)
    bot.reply_to(message, message.text.lower())

@bot.message_handler(content_types=["text"])
def handle_text_message(message: Message):
    if message.chat.type == 'private':
        info(message)
        try:
            answer = gpt4(message.text)
            bot.reply_to(message, answer)
        except Exception as e:
            print(e)
            bot.reply_to(message, "Failed to request. \nTry one more time.")


# Обработчик загрузки документа
@bot.message_handler(content_types=["document"])
def handle_document(message: Message):
    info(message, "handle_document")

    if message.document.mime_type == "text/csv":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name, _ = utils.file_name_type(message.document.file_name)
        # Чтение CSV-файла и преобразование в формат Excel
        responce = elections(BytesIO(downloaded_file))
        responce.name = name + ".xlsx"

        # Отправка файла Excel обратно пользователю
        bot.send_document(message.chat.id, document=responce)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте CSV-файл.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
