import telebot
from DataBaseHeplers.getLanguage import get_language

def ask_diet(user_id : int, bot : telebot.TeleBot, states : dict) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your diet, if You have one. This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите, Вашу диету, если она у Вас есть. Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазначце Вашую дыету, калі ў Вас яна ёсць. Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_diet"

    