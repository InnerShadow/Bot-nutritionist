import os
import pydub
import argparse

import telebot
from telebot import types

from DataBaseHandler import *
from openAiHandler import *

states = {}

def start_dialog(message : telebot.types.Message) -> None:
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English', callback_data = 'English'), 
               types.InlineKeyboardButton('Русский', callback_data = 'Русский'), 
               types.InlineKeyboardButton('Беларуская', callback_data = 'Беларуская'))
    bot.send_message(user_id, "Please choose your language:", reply_markup = markup)

    create_user(user_id)
    update_user_name(user_id, message.from_user.first_name)
    states[user_id] = "start_dialog"


def choose_gender(user_id : int) -> None:

    match get_language(user_id):
        case 0:
            bot.send_message(user_id, "Hello, I am Your personal nutritionist assistant. I am ready to answer any of Your questions in the field of healthy eating, dieting, or just to recommend a snack.\n\nI am also able to calculate the calorie content of the dish on Your photo and respond to Your voice messages.\n\nIn order for my recommendations to be specialized for You, please answer the following questions.")
        case 1:
            bot.send_message(user_id, "Здравствуйте, я Ваш, персональный помошник-нутрициолог. Я готов ответить на любые Ваши вопросы в области здорового питания, диаты или просто посоветовать перекус.\n\nТак же я способен высчитывать колорийность блюда, на Вашей фотографии и отвечать на Ваши голосовые сообщения.\n\nДля того чтобы мои рекоментации были специализированны под Вас, пожалуйста ответте на следующие вопросы.")
        case 2:
            bot.send_message(user_id, "Добры дзень, я Ваш, персанальны памочнік-нутрициолог. Я гатовы адказаць на любыя вашы пытанні ў галіне здаровага харчавання, дыяты ці проста параіць перакус.\n\nТак ж я здольны вылічваць каларыйнасць стравы, на вашай фатаграфіі і адказваць на Вашыя галасавыя паведамленні.\n\nДля таго каб мае рекоментации былі специализированны пад Вас, калі ласка адкажыце на наступныя пытанні.")

    match get_language(user_id):
        case 0:
            male_text = "Male"
            female_text = 'Female'
        case 1: 
            male_text = "Мужчина"
            female_text = 'Женщина'
        case 2:
            male_text = "Мыжчына"
            female_text = 'Жанчына'

    match get_language(user_id):
        case 0:
            response = "Please choose your gender:"
        case 1: 
            response = "Укажите Ваш пол:"
        case 2:
            response = "Калі ласка, пазнацче Ваш пол:"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(male_text, callback_data='Male'), 
               types.InlineKeyboardButton(female_text, callback_data='Female'))
    bot.send_message(user_id, response, reply_markup=markup)
    states[user_id] = "choose_gender"


def ask_height(user_id : int) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your height (in centimetre) . This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите Ваш рост (в сантиметрах). Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазнацче Ваш рост (у сантыметрах). Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_height"


def ask_weight(user_id : int) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your weight (in kilograms) . This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите Ваш вес (в киллограмах). Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазнацче Ваш вес (у кілаграмах). Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_weight"


def ask_purpose(user_id : int) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your purpose of using the bot. This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите цель использования бота. Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазначце цэль выкарыстання даннаго бота. Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_purpose"


def ask_age(user_id : int) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your age. This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите Ваш возраст. Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазначце Ваш узрост. Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_age"


def ask_diet(user_id : int) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your diet, if You have one. This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите, Вашу диету, если она у Вас есть. Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазначце Вашую дыету, калі ў Вас яна ёсць. Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_diet"


def show_users_data(user_id : int) -> None:
    user_data = get_users_data(user_id)
    match get_language(user_id):
        case 0:
            response = f"{user_data[5]}, here is the information you provided: \n\tGender: {user_data[2]};\n\tHeight: {user_data[3]};\n\tWeight: {user_data[4]};\n\tPurpose of using the bot: \"{user_data[6]}\";\n\tDiet: \"{user_data[9]}\"."
        case 1: 
            response = f"{user_data[5]}, вот информация, которую вы предоставили: \n\tПол: {user_data[2]};\n\tРост: {user_data[3]};\n\tВес: {user_data[4]};\n\tЦель использования бота: \"{user_data[6]}\";\n\tДиета: \"{user_data[9]}\"."
        case 2:
            response = f"{user_data[5]}, вось інфармацыя, якую вы пазначылі: \n\tПол: {user_data[2]};\n\tРост: {user_data[3]};\n\tВас: {user_data[4]};\n\tМэта выкарыстанне бота: \"{user_data[6]}\";\n\tДыета: \"{user_data[9]}\"."
    
    bot.send_message(user_id, response)


def handle_callback_query(call : telebot.types.Message) -> None:
    user_id = call.from_user.id
    if user_id not in states:
        start_dialog(call.message)
    elif states[user_id] == "start_dialog":
        chosen_language = call.data
        update_user_language(user_id, chosen_language)
        choose_gender(user_id)
    elif states[user_id] == "choose_gender":
        chosen_gender = call.data
        update_user_gender(user_id, chosen_gender)
        ask_age(user_id)


def handle_text(message : telebot.types.Message) -> None:
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
            ask_height(user_id)
        else:
            match get_language(user_id):
                case 0:
                    response = "Please enter a valid age!"
                case 1: 
                    response = "Пожалуйста, введите Ваш возраст!"
                case 2:
                    response = "Калі ласка, пазначце Ваш узрост!"
            bot.send_message(user_id, response)
            ask_age(user_id)
    elif states[user_id] == "ask_height":
        height = message.text.strip()
        if height.isdigit():
            update_user_height(user_id, float(height))
            ask_weight(user_id)
        else:
            match get_language(user_id):
                case 0:
                    response = "Please enter a valid height!"
                case 1: 
                    response = "Пожалуйста, введите Ваш рост!"
                case 2:
                    response = "Калі ласка, пазначце Ваш рост!"
            bot.send_message(user_id, response)
            ask_height(user_id)
    elif states[user_id] == "ask_weight":
        weight = message.text.strip()
        if weight.isdigit():
            update_user_weight(user_id, float(weight))
            ask_purpose(user_id)
        else:
            match get_language(user_id):
                case 0:
                    response = "Please enter a valid weight!"
                case 1: 
                    response = "Пожалуйста, введите Ваш вес!"
                case 2:
                    response = "Калі ласка, пазначце Ваш вес!"
            bot.send_message(user_id, response)
            ask_weight(user_id)
    elif states[user_id] == "ask_purpose":
        purpose = message.text
        update_user_purpose(user_id, purpose)
        states[user_id] = "ask_diet"
        ask_diet(user_id)
    elif states[user_id] == "ask_diet":
        diet = message.text
        update_user_diet(user_id, diet)
        show_users_data(user_id)
        states[user_id] = 0
    else:
        response = generate_response(openAiToken, message.text, user_id)
        if response == "Error!":
            match get_language(user_id):
                case 0:
                    response = "Sorry, there was an error, maybe Your message is too long."
                case 1: 
                    response = "Извините, возникла ошибка, возможно Ваше сообщение слишком длинное."
                case 2:
                    response = "Выбачайце, узнікла памылка, магчыма Ваша паведамленне занадта доўгае."
            bot.send_message(user_id, response)
            return
        bot.send_message(user_id, response)


def photo_response(message : telebot.types.Message) -> None:
    user_id = message.from_user.id
    if check_chat_existance(user_id):
        if user_id not in states:
            states[user_id] = 0
    else:
        start_dialog(message)
        return
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    caption = message.caption if message.caption else ""

    file_extension = os.path.splitext(file_info.file_path)[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = f"Data/{user_id}_{file_extension}"
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    response = generate_photo_response(openAiToken, save_path, user_id, caption)
    if response == "Error!":
        match get_language(user_id):
            case 0:
                response = "Sorry, there was an error, maybe Your message is too long."
            case 1: 
                response = "Извините, возникла ошибка, возможно Ваше сообщение слишком длинное."
            case 2:
                response = "Выбачайце, узнікла памылка, магчыма Ваша паведамленне занадта доўгае."
        bot.send_message(user_id, response)
        return
    bot.send_message(user_id, response)

    os.remove(save_path)


def voice_response(message : telebot.types.Message) -> None:
    user_id = message.from_user.id
    if check_chat_existance(user_id):
        if user_id not in states:
            states[user_id] = 0
    else:
        start_dialog(message)
        return
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_extension = ".ogg"
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = f"Data/{user_id}_{file_extension}"
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    sound = pydub.AudioSegment.from_file(save_path, format = "ogg")
    sound.export(save_path[:len(save_path) - 3] + ".mp3", format = "mp3")

    response = generate_voise_response(openAiToken, save_path[:len(save_path) - 3] + ".mp3", user_id)
    if response == "Error!":
        match get_language(user_id):
            case 0:
                response = "Sorry, there was an error, maybe Your message is too long."
            case 1: 
                response = "Извините, возникла ошибка, возможно Ваше сообщение слишком длинное."
            case 2:
                response = "Выбачайце, узнікла памылка, магчыма Ваша паведамленне занадта доўгае."
        bot.send_message(user_id, response)
        return

    with open(f"Data/{user_id}.mp3", 'rb') as f:
        bot.send_voice(user_id, f)

    os.remove(save_path)
    os.remove(f"Data/{user_id}.mp3")
    os.remove(save_path[:len(save_path) - 3] + ".mp3")


def main(bot_token: str) -> None:
    global bot
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands = ['start'])
    def start(message):
        start_dialog(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        handle_callback_query(call)

    @bot.message_handler(func = lambda message: True)
    def text_message(message):
        handle_text(message)

    @bot.message_handler(content_types=['photo'])
    def photo_message(message):
        photo_response(message)

    @bot.message_handler(content_types=['voice'])
    def voice_message(message):
        voice_response(message)

    bot.polling(non_stop = True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Telegram Nutritionist Bot ')
    parser.add_argument('bot_token', type=str, help='Telegram Bot token')
    parser.add_argument('openai_token', type=str, help='OpenAI token')
    args = parser.parse_args()
    
    global openAiToken
    openAiToken = args.openai_token
    initDataBase()
    main(args.bot_token)

