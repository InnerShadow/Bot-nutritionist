import os
import pydub
import random
import telebot

from DataBaseHeplers.getLanguage import get_language
from DataBaseHeplers.checkChatExistance import check_chat_existance

from TelebotHeplers.startDialog import start_dialog

from OpenAIHelper.generateVoiseResponse import generate_voise_response

# Function to handle voise input 
def voice_response(message : telebot.types.Message, bot : telebot.TeleBot, states : dict, openAiToken : str) -> None:
    user_id = message.from_user.id
    states[user_id] = 0

    # If user just send voise messge, force him to do /start
    if check_chat_existance(user_id):
        if user_id not in states:
            states[user_id] = 0
    else:
        start_dialog(message, bot, states)
        return
    
    # Get audio file from telegram and download it
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_extension = ".ogg"
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = f"Data/{user_id}_{random.randint(0, 10000)}_{file_extension}"
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Convert file inpu .mp3 format 
    sound = pydub.AudioSegment.from_file(save_path, format = "ogg")
    sound.export(save_path[:len(save_path) - 3] + ".mp3", format = "mp3")

    # Use OPEN AI IPI to preprocess voice input
    response = generate_voise_response(openAiToken, save_path[:len(save_path) - 3] + ".mp3", user_id)

    # If OPEN AI IPI throw error say user about it
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

    # Response with voice message 
    with open(f"Data/{user_id}.mp3", 'rb') as f:
        bot.send_voice(user_id, f)

    # Remove temporary files
    os.remove(save_path)
    os.remove(f"Data/{user_id}.mp3")
    os.remove(save_path[:len(save_path) - 3] + ".mp3")

