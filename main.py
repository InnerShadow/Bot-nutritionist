import telebot
from telebot import types
import argparse
from DataBase.DataBaseHandler import *
from openAiHandler import *

states = {}

def start_dialog(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English', callback_data='English'), 
               types.InlineKeyboardButton('Русский', callback_data='Русский'), 
               types.InlineKeyboardButton('Беларуская', callback_data='Беларуская'))
    bot.send_message(user_id, "Please choose your language:", reply_markup=markup)

    create_user(user_id)
    update_user_name(user_id, message.from_user.first_name)
    states[user_id] = "start_dialog"


def choose_gender(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Male', callback_data='Male'), 
               types.InlineKeyboardButton('Female', callback_data='Female'))
    bot.send_message(user_id, "Please choose your gender:", reply_markup=markup)
    states[user_id] = "choose_gender"


def ask_height(user_id):
    bot.send_message(user_id, "Please enter your height (in centimeters):")
    states[user_id] = "ask_height"


def ask_weight(user_id):
    bot.send_message(user_id, "Please enter your weight (in kilograms):")
    states[user_id] = "ask_weight"


def ask_purpose(user_id):
    bot.send_message(user_id, "Please enter your purpose of using this bot:")
    states[user_id] = "ask_purpose"


def ask_age(user_id):
    bot.send_message(user_id, "Please enter your age (in years):")
    states[user_id] = "ask_age"


def show_users_data(user_id):
    response = get_users_data(user_id)
    bot.send_message(user_id, response)


def handle_callback_query(call):
    user_id = call.from_user.id
    if user_id not in states:
        start_dialog(call.message)
    elif states[user_id] == "start_dialog":
        chosen_language = call.data
        update_user_language(user_id, chosen_language)
        bot.send_message(user_id, f"You have chosen {chosen_language} language.")
        choose_gender(user_id)
    elif states[user_id] == "choose_gender":
        chosen_gender = call.data
        update_user_gender(user_id, chosen_gender)
        bot.send_message(user_id, f"You have chosen {chosen_gender} gender.")
        ask_age(user_id)


def handle_text(message):
    user_id = message.from_user.id
    if check_chat_existance(user_id):
        if user_id not in states:
            states[user_id] = 0
    else:
        start_dialog(message)
        return
    
    if states[user_id] == "ask_age":
        age = message.text.strip()
        if age.isdigit():
            update_user_age(user_id, float(age))
            bot.send_message(user_id, f"Your age {age} years has been saved.")
            ask_height(user_id)
        else:
            bot.send_message(user_id, "Please enter a valid age.")
            ask_age(user_id)
    elif states[user_id] == "ask_height":
        height = message.text.strip()
        if height.isdigit():
            update_user_height(user_id, float(height))
            bot.send_message(user_id, f"Your height {height} cm has been saved.")
            ask_weight(user_id)
        else:
            bot.send_message(user_id, "Please enter a valid height.")
            ask_height(user_id)
    elif states[user_id] == "ask_weight":
        weight = message.text.strip()
        if weight.isdigit():
            update_user_weight(user_id, float(weight))
            bot.send_message(user_id, f"Your weight {weight} kg has been saved.")
            ask_purpose(user_id)
        else:
            bot.send_message(user_id, "Please enter a valid weight.")
            ask_weight(user_id)
    elif states[user_id] == "ask_purpose":
        purpose = message.text
        update_user_purpose(user_id, purpose)
        bot.send_message(user_id, f"Your are goin to use this bot for \"{purpose}\" purpose.")
        show_users_data(user_id)
        states[user_id] = 0
    else:
        bot.send_message(user_id, generate_response(openAiToken, message.text, user_id))


def main(bot_token: str) -> None:
    global bot
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=['start'])
    def start(message):
        start_dialog(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        handle_callback_query(call)

    @bot.message_handler(func = lambda message: True)
    def text_message(message):
        handle_text(message)

    bot.polling(non_stop=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Telegram Nutritionist Bot ')
    parser.add_argument('bot_token', type=str, help='Telegram Bot token')
    parser.add_argument('openai_token', type=str, help='OpenAI token')
    args = parser.parse_args()
    
    global openAiToken
    openAiToken = args.openai_token
    initDataBase()
    main(args.bot_token)
