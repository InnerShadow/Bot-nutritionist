import telebot
from DataBaseHandler import get_language

def ask_purpose(user_id : int, bot : telebot.TeleBot, states : dict) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your purpose of using the bot. This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите цель использования бота. Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазначце цэль выкарыстання даннаго бота. Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_purpose"