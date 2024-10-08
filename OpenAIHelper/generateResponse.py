from openai import OpenAI

from DataBaseHeplers.getUsersData import get_users_data
from DataBaseHeplers.getMessageHistory import getMessageHistory
from DataBaseHeplers.insertMessage import insertMessage

# Function to generate response on text message
def generate_response(token : str, message : str, user_id : int, doSave = True) -> str:
    client = OpenAI(api_key = token)
    try:
        # Get user's prev 10 messages
        user_data = get_users_data(user_id)

        # Get nutritionist specialist as target to Chat GPT
        history = []
        history.append({
                        'role' : "system", 
                        "content" : "You are nutritionist specialist. Aswer only questions from you're scope of knowledge."
                        })
        
        # Give Chat more inpormation about user
        history.append({
                        'role' : "user", 
                        "content" : f"""My name is {user_data[5]}, i am {user_data[2]}, i am {user_data[8]} years old, 
                                    my hight is {user_data[3]} cm, my weight is {user_data[4]} kg, i ask question for \"{user_data[6]}\", 
                                    my diet is : \"{user_data[9]}\". Call me by my first name and use this information about my health condition in the response."""
                        })    
        
        # add append all other prev messages
        for mesg, role in reversed(getMessageHistory(user_id)):
            history.append({'role': role, 'content': mesg})

        # And ask to new question
        history.append({'role' : "user", "content" : f"Answer next question: {message}"})

        # Get response from OPEN AI API
        response = client.chat.completions.create(
            model = 'gpt-4-turbo',
            messages = history
        )

        # Preprosess response
        answer = response.choices[0].message.content.replace("*", "").replace("#", "")

        # Save answers if need
        if doSave:
            insertMessage(user_id, message, "user")
            insertMessage(user_id, answer, "system")

        return answer
    except Exception as e:
        return "Error!"

