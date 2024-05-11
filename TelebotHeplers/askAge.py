import telebot
from DataBaseHeplers.getLanguage import get_language

# Function to ask user age
def ask_age(user_id : int, bot : telebot.TeleBot, states : dict) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your age. This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите Ваш возраст. Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазначце Ваш узрост. Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_age"

