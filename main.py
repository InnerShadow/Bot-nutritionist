import telebot
from telebot import types
import argparse

def main(bot_token: str) -> None:
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands = ['start'])
    def start_handler(message: telebot.types.Message) -> None:
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('English', callback_data = 'English')
        itembtn2 = types.InlineKeyboardButton('Русский', callback_data = 'Русский')
        itembtn3 = types.InlineKeyboardButton('Беларуская', callback_data = 'Беларуская')
        markup.row(itembtn1)
        markup.row(itembtn2)
        markup.row(itembtn3)
        bot.send_message(message.chat.id, "Please choose your language:", reply_markup = markup)

    bot.polling(non_stop = True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Telegram Nutritionist Bot ')
    parser.add_argument('bot_token', type = str, help = 'Telegram Bot token')
    args = parser.parse_args()
    
    main(args.bot_token)
