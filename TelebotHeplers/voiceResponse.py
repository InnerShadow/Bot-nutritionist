import os
import pydub
import telebot

from DataBaseHeplers.getLanguage import get_language
from DataBaseHeplers.checkChatExistance import check_chat_existance

from TelebotHeplers.startDialog import start_dialog

from OpenAIHelper.generateVoiseResponse import generate_voise_response

def voice_response(message : telebot.types.Message, bot : telebot.TeleBot, states : dict, openAiToken : str) -> None:
    user_id = message.from_user.id
    states[user_id] = 0
    if check_chat_existance(user_id):
        if user_id not in states:
            states[user_id] = 0
    else:
        start_dialog(message, bot, states)
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

