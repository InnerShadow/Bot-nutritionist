from openai import OpenAI
from DataBase.DataBaseHandler import *

def generate_response(token : str, message : str, user_id : int) -> str:
    client = OpenAI(api_key = token)

    user_data = get_users_data(user_id)

    history = []
    history.append({'role' : "system", "content" : "You are nutritionist specialist."})
    history.append({'role' : "user", "content" : f"I am {user_data[5]}, i am {user_data[2]}, i am {user_data[8]} years old, i am {user_data[3]}, i am {user_data[4]}, i am goint to use this you for \"{user_data[6]}\"."})    
    for mesg, role in getMessageHistory(user_id):
        history.append({'role': role, 'content': mesg})

    history.append({'role' : "user", "content" : f"Answer next question: {message}"})

    response = client.chat.completions.create(
        model = 'gpt-4-turbo',
        messages = history
    )

    answer = response.choices[0].message.content.replace("*", "")

    insertMessage(user_id, message, "user")
    insertMessage(user_id, answer, "system")

    return answer