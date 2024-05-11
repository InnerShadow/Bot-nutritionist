import telebot
from DataBaseHandler import get_language, update_user_language, update_user_gender

from TelebotHeplers.startDialog import start_dialog
from TelebotHeplers.chooseGender import choose_gender
from TelebotHeplers.askAge import ask_age

def handle_callback_query(call : telebot.types.Message, bot : telebot.TeleBot, states : dict) -> None:
    user_id = call.from_user.id
    if user_id not in states:
        start_dialog(call.message, bot, states)
    elif call.data == "Skip":
         states[user_id] = 0
         match get_language(user_id):
            case 0:
                response = "I am ready to answer any of your questions!!!"
            case 1: 
                response = "Я готов ответить на любые Ваши вопросы!!!"
            case 2:
                response = "Я гатовы адказаць на любыя вашы пытанні!!!"
    
         bot.send_message(user_id, response)
    elif states[user_id] == "start_dialog":
        chosen_language = call.data
        update_user_language(user_id, chosen_language)
        choose_gender(user_id, bot, states)
    elif states[user_id] == "choose_gender":
        chosen_gender = call.data
        update_user_gender(user_id, chosen_gender)
        ask_age(user_id, bot, states)

