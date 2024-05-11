from openai import OpenAI

from DataBaseHandler import *

def generate_response(token : str, message : str, user_id : int, doSave = True) -> str:
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

        history.append({'role' : "user", "content" : f"Answer next question: {message}"})

        response = client.chat.completions.create(
            model = 'gpt-4-turbo',
            messages = history
        )

        answer = response.choices[0].message.content.replace("*", "").replace("#", "")

        if doSave:
            insertMessage(user_id, message, "user")
            insertMessage(user_id, answer, "system")

        return answer
    except Exception as e:
        return "Error!"

