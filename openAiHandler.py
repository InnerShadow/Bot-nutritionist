from openai import OpenAI
from DataBase.DataBaseHandler import *
import base64
import requests

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

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_photo_response(token : str, photo : str, user_id : int, caption : str) -> str:
    client = OpenAI(api_key = token)

    user_data = get_users_data(user_id)

    history = []
    history.append({'role' : "system", "content" : "You are nutritionist specialist."})
    history.append({'role' : "user", "content" : f"I am {user_data[5]}, i am {user_data[2]}, i am {user_data[8]} years old, i am {user_data[3]}, i am {user_data[4]}, i am goint to use this you for \"{user_data[6]}\"."})    
    for mesg, role in getMessageHistory(user_id):
        history.append({'role': role, 'content': mesg})

    base64_image = encode_image(photo)
    
    response = client.chat.completions.create(
        model = "gpt-4-vision-preview",
        messages = history + [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Predict number of the proteins\\fats\\carbohydrates and calorie content on image. " + caption + ". In your reply, use the language from the previous correspondence."},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ]
    )


    history.append({'role' : "user", "type" : "text" ,"content" : "Что на фотографии"})
    history.append({'role' : "user", "type" : "image_url" ,"content" : f"data:image/jpeg;base64,{base64_image}", "detail": "low"})

    answer = response.choices[0].message.content.replace("*", "")

    insertMessage(user_id, "Image", "user")
    insertMessage(user_id, answer, "system")

    return answer