import telebot
from DataBaseHeplers.getLanguage import get_language

# function to ask user the height
def ask_height(user_id : int, bot : telebot.TeleBot, states : dict) -> None:
    match get_language(user_id):
        case 0:
            response = "Please specify Your height (in centimetre) . This is required for more accurate nutritionist recommendations."
        case 1: 
            response = "Укажите Ваш рост (в сантиметрах). Это необходимо для более точных рекомендаций нутрициолога."
        case 2:
            response = "Калі ласка, пазнацче Ваш рост (у сантыметрах). Гэта неабходна для больш дакладных рэкамендацый нутрыцыялога."
    bot.send_message(user_id, response)
    states[user_id] = "ask_height"
