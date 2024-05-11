from telebot import types
import telebot

from DataBaseHeplers.updateUserName import update_user_name
from DataBaseHeplers.createUser import create_user

# Start dialog with langusge choise 
def start_dialog(message : telebot.types.Message, bot : telebot.TeleBot, states : dict) -> None:
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('English', callback_data = 'English'), 
               types.InlineKeyboardButton('Русский', callback_data = 'Русский'), 
               types.InlineKeyboardButton('Беларуская', callback_data = 'Беларуская'))
    bot.send_message(user_id, "Please choose your language:", reply_markup = markup)

    create_user(user_id)
    update_user_name(user_id, message.from_user.first_name)
    states[user_id] = "start_dialog"

