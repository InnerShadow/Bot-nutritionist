import telebot
from DataBaseHandler import get_language

def help_dialog(message : telebot.types.Message, bot : telebot.TeleBot) -> None:
    user_id = message.from_user.id
    match get_language(user_id):
        case 0:
            bot.send_message(user_id, "Hello, I am Your personal nutritionist assistant. I am ready to answer any of Your questions in the field of healthy eating, dieting, or just to recommend a snack.\n\nI am also able to calculate the calorie content of the dish on Your photo and respond to Your voice messages.\n\nIn order for my recommendations to be specialized for You, please answer the following questions.")
        case 1:
            bot.send_message(user_id, "Здравствуйте, я Ваш, персональный помошник-нутрициолог. Я готов ответить на любые Ваши вопросы в области здорового питания, диаты или просто посоветовать перекус.\n\nТак же я способен высчитывать колорийность блюда, на Вашей фотографии и отвечать на Ваши голосовые сообщения.\n\nДля того чтобы мои рекоментации были специализированны под Вас, пожалуйста ответте на следующие вопросы.")
        case 2:
            bot.send_message(user_id, "Добры дзень, я Ваш, персанальны памочнік-нутрициолог. Я гатовы адказаць на любыя вашы пытанні ў галіне здаровага харчавання, дыяты ці проста параіць перакус.\n\nТак ж я здольны вылічваць каларыйнасць стравы, на вашай фатаграфіі і адказваць на Вашыя галасавыя паведамленні.\n\nДля таго каб маі рэкамендацыі былі специализированны пад Вас, калі ласка адкажыце на наступныя пытанні.")
