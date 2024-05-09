from openai import OpenAI
from DataBaseHandler import *
import base64
from pathlib import Path

def generate_response(token : str, message : str, user_id : int, doSave = True) -> str:
    client = OpenAI(api_key = token)
    try:
        user_data = get_users_data(user_id)

        history = []
        history.append({'role' : "system", "content" : "You are nutritionist specialist. Aswer only questions from you're scope of knowledge."})
        history.append({'role' : "user", "content" : f"My name is {user_data[5]}, i am {user_data[2]}, i am {user_data[8]} years old, my hight is {user_data[3]} cm, my weight is {user_data[4]} kg, i ask question for \"{user_data[6]}\", my diet is : \"{user_data[9]}\". Call me by my first name and use this information in the response."})    
        for mesg, role in getMessageHistory(user_id):
            history.append({'role': role, 'content': mesg})

        history.append({'role' : "user", "content" : f"Answer next question: {message}"})

        response = client.chat.completions.create(
            model = 'gpt-4-turbo',
            messages = history
        )

        answer = response.choices[0].message.content.replace("*", "")

        if doSave:
            insertMessage(user_id, message, "user")
            insertMessage(user_id, answer, "system")

        return answer
    except Exception:
        return "Error!"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_photo_response(token : str, photo : str, user_id : int, caption : str) -> str:
    client = OpenAI(api_key = token)
    try:
        user_data = get_users_data(user_id)

        history = []
        history.append({'role' : "system", "content" : "You are nutritionist specialist. Aswer only questions from you're scope of knowledge."})
        history.append({'role' : "user", "content" : f"My name is {user_data[5]}, i am {user_data[2]}, i am {user_data[8]} years old, my hight is {user_data[3]} cm, my weight is {user_data[4]} kg, i ask question for \"{user_data[6]}\", my diet is : \"{user_data[9]}\". Call me by my first name and use this information in the response."})    
        for mesg, role in getMessageHistory(user_id):
            history.append({'role': role, 'content': mesg})

        base64_image = encode_image(photo)
        
        response = client.chat.completions.create(
            model = "gpt-4-vision-preview",
            messages = history + [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Predict number of the proteins\\fats\\carbohydrates and calorie content on image. " + caption + ". In your reply, use the language from the previous correspondence. Call me by my first name and use this information in the response."},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ]
        )

        answer = response.choices[0].message.content.replace("*", "")

        insertMessage(user_id, "Image", "user")
        insertMessage(user_id, answer, "system")

        return answer
    except Exception:
        return "Error!"

def generate_voise_response(token : str, voice : str, user_id : int) -> str:
    client = OpenAI(api_key = token)

    try:
        user_data = get_users_data(user_id)

        history = []
        history.append({'role' : "system", "content" : "You are nutritionist specialist. Aswer only questions from you're scope of knowledge."})
        history.append({'role' : "user", "content" : f"My name is {user_data[5]}, i am {user_data[2]}, i am {user_data[8]} years old, my hight is {user_data[3]} cm, my weight is {user_data[4]} kg, i ask question for \"{user_data[6]}\", my diet is : \"{user_data[9]}\". Call me by my first name and use this information in the response."})    
        for mesg, role in getMessageHistory(user_id):
            history.append({'role': role, 'content': mesg})

        audio_file = open(voice, "rb")
        transcription = client.audio.transcriptions.create(
            model = "whisper-1", 
            file = audio_file
        )

        insertMessage(user_id, transcription.text, "user")
        answer = generate_response(token, transcription.text, user_id, False)
        insertMessage(user_id, answer, "system")

        speech_file_path = Path(__file__).parent / f"Data/{user_id}.mp3"
        response = client.audio.speech.create(
            model = "tts-1",
            voice = "alloy",
            input = answer
        )

        response.stream_to_file(speech_file_path)
        
        return answer
    except Exception:
        return "Error!"
