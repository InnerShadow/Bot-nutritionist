from openai import OpenAI
from DataBase.DataBaseHandler import insertMessage

def generate_response(token : str, message : str, user_id : int) -> str:
    client = OpenAI(api_key = token)
    response = client.chat.completions.create(
        model = 'gpt-4-turbo',
        messages = [
            {'role' : "user", "content" : f"Ask next question: {message}"} 
        ]
    )

    insertMessage(user_id, message)
    insertMessage(user_id, response.choices[0].message.content)

    return response.choices[0].message.content