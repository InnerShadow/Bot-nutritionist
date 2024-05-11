from openai import OpenAI
from DataBaseHandler import *
from pathlib import Path

from OpenAIHelper.generateResponse import generate_response

def generate_voise_response(token : str, voice : str, user_id : int) -> str:
    client = OpenAI(api_key = token)

    try:
        user_data = get_users_data(user_id)

        history = []
        history.append({
                        'role' : "system", 
                        "content" : "You are nutritionist specialist. Aswer only questions from you're scope of knowledge."
                        })

        history.append({
                        'role' : "user", 
                        "content" : f"""My name is {user_data[5]}, i am {user_data[2]}, i am {user_data[8]} years old,
                                        my hight is {user_data[3]} cm, my weight is {user_data[4]} kg, i ask question for \"{user_data[6]}\", 
                                        my diet is : \"{user_data[9]}\". Call me by my first name and use this information about my health condition in the response."""
                        })    
        
        for mesg, role in reversed(getMessageHistory(user_id)):
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

