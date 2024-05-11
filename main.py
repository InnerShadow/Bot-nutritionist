import telebot
import argparse

from DataBaseHeplers.initDataBase import initDataBase

from TelebotHeplers.startDialog import start_dialog
from TelebotHeplers.helpDialog import help_dialog
from TelebotHeplers.showUsersData import show_users_data
from TelebotHeplers.handleCallbackQuery import handle_callback_query
from TelebotHeplers.handleText import handle_text
from TelebotHeplers.photoResponse import photo_response
from TelebotHeplers.voiceResponse import voice_response

states = {}

def main(bot_token: str) -> None:
    global bot
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands = ['start'])
    def start(message : telebot.types.Message) -> None:
        start_dialog(message, bot, states)

    @bot.message_handler(commands = ['help'])
    def help(message : telebot.types.Message) -> None:
        help_dialog(message, bot)

    @bot.message_handler(commands = ['info'])
    def info(message : telebot.types.Message) -> None:
        show_users_data(message.from_user.id)

    @bot.callback_query_handler(func = lambda call: True)
    def callback_query(call : telebot.types.Message) -> None:
        handle_callback_query(call, bot, states)

    @bot.message_handler(func = lambda message: True)
    def text_message(message : telebot.types.Message) -> None:
        handle_text(message, bot, states, openAiToken)

    @bot.message_handler(content_types = ['photo'])
    def photo_message(message : telebot.types.Message) -> None:
        photo_response(message, bot, states)

    @bot.message_handler(content_types = ['voice'])
    def voice_message(message : telebot.types.Message) -> None:
        voice_response(message, bot, states)

    bot.polling(non_stop = True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Telegram Nutritionist Bot ')
    parser.add_argument('bot_token', type = str, help = 'Telegram Bot token')
    parser.add_argument('openai_token', type = str, help = 'OpenAI token')
    args = parser.parse_args()
    
    global openAiToken
    openAiToken = args.openai_token
    initDataBase()
    main(args.bot_token)

