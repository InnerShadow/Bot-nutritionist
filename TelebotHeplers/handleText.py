import telebot

from OpenAIHelper.generateResponse import generate_response

from TelebotHeplers.startDialog import start_dialog
from TelebotHeplers.askHeight import ask_height
from TelebotHeplers.askAge import ask_age
from TelebotHeplers.askWeight import ask_weight
from TelebotHeplers.askDiet import ask_diet
from TelebotHeplers.askPupoise import ask_purpose
from TelebotHeplers.showUsersData import show_users_data

from DataBaseHeplers.checkChatExistance import check_chat_existance
from DataBaseHeplers.getLanguage import get_language
from DataBaseHeplers.updateUserAge import update_user_age
from DataBaseHeplers.updateUserHeight import update_user_height
from DataBaseHeplers.updateUserWeight import update_user_weight
from DataBaseHeplers.updateUserPurpose import update_user_purpose
from DataBaseHeplers.updateUserDiet import update_user_diet

# function to handle text messages
def handle_text(message : telebot.types.Message, bot : telebot.TeleBot, states : dict, openAiToken : str) -> None:
    user_id = message.from_user.id

    # Forse user to do /start if he just start tupping messages
    if check_chat_existance(user_id):
        if user_id not in states:
            states[user_id] = 0
    else:
        start_dialog(message, bot, states)
        return
    
    # Ask user age
    if states[user_id] == "ask_age":
        age = message.text.strip()
        if age.isdigit():
            update_user_age(user_id, float(age))
            ask_height(user_id, bot, states)
        else:
            # If user send not a number, ask to send again 
            match get_language(user_id):
                case 0:
                    response = "Please enter a valid age!"
                case 1: 
                    response = "Пожалуйста, введите Ваш возраст!"
                case 2:
                    response = "Калі ласка, пазначце Ваш узрост!"
            bot.send_message(user_id, response)
            ask_age(user_id, bot, states)

    # Ask user a height
    elif states[user_id] == "ask_height":
        height = message.text.strip()
        if height.isdigit():
            update_user_height(user_id, float(height))
            ask_weight(user_id, bot, states)
        else:
            # If user send not a number, ask to send again 
            match get_language(user_id):
                case 0:
                    response = "Please enter a valid height!"
                case 1: 
                    response = "Пожалуйста, введите Ваш рост!"
                case 2:
                    response = "Калі ласка, пазначце Ваш рост!"
            bot.send_message(user_id, response)
            ask_height(user_id, bot, states)

    # Ask user a weight
    elif states[user_id] == "ask_weight":
        weight = message.text.strip()
        if weight.isdigit():
            update_user_weight(user_id, float(weight))
            ask_purpose(user_id, bot, states)
        else:
            # If user send not a number, ask to send again 
            match get_language(user_id):
                case 0:
                    response = "Please enter a valid weight!"
                case 1: 
                    response = "Пожалуйста, введите Ваш вес!"
                case 2:
                    response = "Калі ласка, пазначце Ваш вес!"
            bot.send_message(user_id, response)
            ask_weight(user_id, bot, states)

    # Ask user a purpose of using this bot
    elif states[user_id] == "ask_purpose":
        purpose = message.text
        update_user_purpose(user_id, purpose)
        states[user_id] = "ask_diet"
        ask_diet(user_id, bot, states)
    
    # Ask user a diet
    elif states[user_id] == "ask_diet":
        diet = message.text
        update_user_diet(user_id, diet)
        show_users_data(user_id, bot)
        states[user_id] = 0

    # Generate text response from Open AI
    else:
        response = generate_response(openAiToken, message.text, user_id)

        # If Open AI API throw a Error, say user about this
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

