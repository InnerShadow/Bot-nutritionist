import telebot
from DataBaseHandler import get_language, get_users_data

def show_users_data(user_id : int, bot : telebot.TeleBot) -> None:
    user_data = list(get_users_data(user_id))
    match get_language(user_id):
        case 0:
            pass
        case 1: 
            match user_data[2]:
                case "Male":
                    user_data[2] = "Мужчина"
                case "Female":
                    user_data[2] = "Женщина"
        case 2:
            match user_data[2]:
                case "Male":
                    user_data[2] = "Мужчыны"
                case "Female":
                    user_data[2] = "Жанчына"
    match get_language(user_id):
        case 0:
            response = f"{user_data[5]}, here is the information you provided: \n\tGender: {user_data[2]};\n\tHeight: {user_data[3]};\n\tWeight: {user_data[4]};\n\tPurpose of using the bot: \"{user_data[6]}\";\n\tDiet: \"{user_data[9]}\"."
        case 1: 
            response = f"{user_data[5]}, вот информация, которую вы предоставили: \n\tПол: {user_data[2]};\n\tРост: {user_data[3]};\n\tВес: {user_data[4]};\n\tЦель использования бота: \"{user_data[6]}\";\n\tДиета: \"{user_data[9]}\"."
        case 2:
            response = f"{user_data[5]}, вось інфармацыя, якую вы пазначылі: \n\tПол: {user_data[2]};\n\tРост: {user_data[3]};\n\tВас: {user_data[4]};\n\tМэта выкарыстанне бота: \"{user_data[6]}\";\n\tДыета: \"{user_data[9]}\"."
    
    bot.send_message(user_id, response)

