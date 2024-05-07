import telebot
from telebot import types
import argparse
from DataBase.DataBaseHandler import *

states = {}

def start_dialog(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English', callback_data='English'), 
               types.InlineKeyboardButton('Русский', callback_data='Русский'), 
               types.InlineKeyboardButton('Беларуская', callback_data='Беларуская'))
    bot.send_message(user_id, "Please choose your language:", reply_markup=markup)
    states[user_id] = 'choose_language'


def handle_language(message):
    user_id = message.from_user.id
    language = message.text
    if language in ['English', 'Русский', 'Беларуская']:
        create_user(user_id, language)
        bot.send_message(user_id, "Please provide your sex (1 for male, 2 for female):")
        states[user_id] = 'choose_sex'
    else:
        bot.send_message(user_id, "Invalid language choice. Please choose again.")


def handle_sex(message):
    user_id = message.from_user.id
    sex = message.text
    if sex in ['1', '2']:
        update_user_sex(user_id, int(sex))
        bot.send_message(user_id, "Please provide your height (in meters):")
        states[user_id] = 'choose_height'
    else:
        bot.send_message(user_id, "Invalid sex choice. Please choose again.")


def handle_height(message):
    user_id = message.from_user.id
    height = message.text
    try:
        height = float(height)
        update_user_height(user_id, height)
        bot.send_message(user_id, "Please provide your weight (in kilograms):")
        states[user_id] = 'choose_weight'
    except ValueError:
        bot.send_message(user_id, "Invalid height format. Please provide your height again (in meters):")


def handle_weight(message):
    user_id = message.from_user.id
    weight = message.text
    try:
        weight = float(weight)
        update_user_weight(user_id, weight)
        bot.send_message(user_id, "Thank you! Your information has been recorded.")
        states.pop(user_id)
    except ValueError:
        bot.send_message(user_id, "Invalid weight format. Please provide your weight again (in kilograms):")


def main(bot_token: str) -> None:
    global bot
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=['start'])
    def start(message):
        start_dialog(message)

    @bot.message_handler(func=lambda message: states.get(message.from_user.id) == 'choose_language')
    def language_handler(message):
        handle_language(message)

    @bot.message_handler(func=lambda message: states.get(message.from_user.id) == 'choose_sex')
    def sex_handler(message):
        handle_sex(message)

    @bot.message_handler(func=lambda message: states.get(message.from_user.id) == 'choose_height')
    def height_handler(message):
        handle_height(message)

    @bot.message_handler(func=lambda message: states.get(message.from_user.id) == 'choose_weight')
    def weight_handler(message):
        handle_weight(message)

    bot.polling(non_stop=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Telegram Nutritionist Bot ')
    parser.add_argument('bot_token', type=str, help='Telegram Bot token')
    args = parser.parse_args()

    initDataBase()
    main(args.bot_token)