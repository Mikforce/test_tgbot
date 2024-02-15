# python -m pip install requests
# t.me/E_a_s_y_B_bot
# pip install pyTelegramBotAPI

import telebot
import requests
import logging

# Настройка логирования
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Создание нового экземпляра Telebot
bot = telebot.TeleBot("6683335183:AAEhsKQrOgmrxpwSIklhBKAUEM5eyGLJqRo")

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def start(message):
    logging.info(f"User {message.chat.id} used /start command")
    bot.reply_to(message, "Привет! Я бот для конвертации валют. Используй /help для просмотра доступных команд.")


# Функция для обработки команды /help
@bot.message_handler(commands=['help'])
def help_message(message):
    logging.info(f"User {message.chat.id} used /help command")
    bot.reply_to(message, '''Доступные команды:
/convert <сумма> <валюта_from> в <валюта_to> - конвертация валюты
Например: /convert 100 USD в EUR''')

# Функция для обработки команды /convert
@bot.message_handler(commands=['convert'])
def convert_currency(message):
    logging.info(f"User {message.chat.id} used /convert command")
    text = message.text.split()

    if len(text) != 5 or text[0] != '/convert':
        bot.reply_to(message, 'Неверный формат команды. Используйте /convert <сумма> <валюта_from> в <валюта_to>.')
        return

    amount = float(text[1])
    base_currency = text[2].upper()
    target_currency = text[4].upper()

    response = requests.get(f'https://v6.exchangerate-api.com/v6/17dc55b325f19c23cf70ea94/latest/{base_currency}')
    data = response.json()

    if target_currency in data['conversion_rates']:
        result = amount * data['conversion_rates'][target_currency]
        bot.reply_to(message, f'{amount} {base_currency} равно {result} {target_currency}.')
    else:
        bot.reply_to(message, 'Невозможно конвертировать указанные валюты.')

# Функция для обработки текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    logging.info(f"User {message.chat.id} sent a text message")

    text = message.text.lower()
    if 'привет' in text:
        bot.reply_to(message, 'Привет!')
    elif 'пока' in text:
        bot.reply_to(message, 'Пока!')
    else:
        bot.reply_to(message, 'Я не понимаю.')

# Опрос сервера для получения обновлений
bot.polling()