import telebot
import os

from DataBaseHeplers.checkChatExistance import check_chat_existance
from DataBaseHeplers.getLanguage import get_language

from TelebotHeplers.startDialog import start_dialog

from OpenAIHelper.generatePhotoResponse import generate_photo_response 

def photo_response(message : telebot.types.Message, bot : telebot.TeleBot, states : dict, openAiToken : str) -> None:
    user_id = message.from_user.id
    states[user_id] = 0
    if check_chat_existance(user_id):
        if user_id not in states:
            states[user_id] = 0
    else:
        start_dialog(message, bot, states)
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

