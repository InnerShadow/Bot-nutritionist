import telebot
from telebot import types
from DataBaseHeplers.getLanguage import get_language

def choose_gender(user_id : int, bot : telebot.TeleBot, states : dict) -> None:
    match get_language(user_id):
        case 0:
            bot.send_message(user_id, "Hello, I am Your personal nutritionist assistant. I am ready to answer any of Your questions in the field of healthy eating, dieting, or just to recommend a snack.\n\nI am also able to calculate the calorie content of the dish on Your photo and respond to Your voice messages.\n\nIn order for my recommendations to be specialized for You, please answer the following questions.\nTo get information about the bot, use /help.\nTo get information about you, use /info.\n")
        case 1:
            bot.send_message(user_id, "Здравствуйте, я Ваш, персональный помошник-нутрициолог. Я готов ответить на любые Ваши вопросы в области здорового питания, диаты или просто посоветовать перекус.\n\nТак же я способен высчитывать колорийность блюда, на Вашей фотографии и отвечать на Ваши голосовые сообщения.\n\nДля того чтобы мои рекоментации были специализированны под Вас, пожалуйста ответте на следующие вопросы.\nДля получения информации о боте используйте /help.\nДля получения информации о Вас используйте /info.\n")
        case 2:
            bot.send_message(user_id, "Добры дзень, я Ваш, персанальны памочнік-нутрициолог. Я гатовы адказаць на любыя вашы пытанні ў галіне здаровага харчавання, дыяты ці проста параіць перакус.\n\nТак ж я здольны вылічваць каларыйнасць стравы, на вашай фатаграфіі і адказваць на Вашыя галасавыя паведамленні.\n\nДля таго каб маі рэкамендацыі былі специализированны пад Вас, калі ласка адкажыце на наступныя пытанні.\n Каб атрымаць інфармацыю аб боце выкарыстоўвайце /help.\nКаб атрымаць інфармацыю пра Вас выкарыстоўвайце /info.\n")

    match get_language(user_id):
        case 0:
            male_text = "Male"
            female_text = 'Female'
            skip_text = "Skip all questions"
        case 1: 
            male_text = "Мужчина"
            female_text = 'Женщина'
            skip_text = "Пропустить все вопросы"
        case 2:
            male_text = "Мыжчына"
            female_text = 'Жанчына'
            skip_text = "Прапусціць усе пытанні"

    match get_language(user_id):
        case 0:
            response = "Please choose your gender:"
        case 1: 
            response = "Укажите Ваш пол:"
        case 2:
            response = "Калі ласка, пазнацче Ваш пол:"
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(male_text, callback_data = 'Male')
    btn2 = types.InlineKeyboardButton(female_text, callback_data = 'Female')
    btn3 = types.InlineKeyboardButton(skip_text, callback_data = 'Skip')
    markup.row(btn1, btn2)
    markup.row(btn3)
    bot.send_message(user_id, response, reply_markup = markup)
    states[user_id] = "choose_gender"

