import telebot
from DataBaseHeplers.getLanguage import get_language

def ask_weight(user_id : int, bot : telebot.TeleBot, states : dict) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your weight (in kilograms) . This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите Ваш вес (в киллограмах). Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазнацче Ваш вес (у кілаграмах). Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_weight"

