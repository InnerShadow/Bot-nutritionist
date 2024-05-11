from openai import OpenAI
from DataBaseHandler import *
import base64
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

def reduce_image_quality(image_path, quality):
    img = Image.open(image_path)
    img.save(image_path, quality = quality)


def generate_photo_response(token : str, photo : str, user_id : int, caption : str) -> str:
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

        base64_image = encode_image(photo)
        quality = 90
        while len(base64_image) < 86_000:
            reduce_image_quality(photo, quality)
            quality -= 5
            base64_image = encode_image(photo)
        
        response = client.chat.completions.create(
            model = "gpt-4-vision-preview",
            messages = history + [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": """Predict number of the proteins\\fats\\carbohydrates and calorie content on image. " + caption + ".
                                        In your reply, use the language from the previous correspondence."""},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ]
        )

        answer = response.choices[0].message.content.replace("*", "").replace("#", "")

        insertMessage(user_id, "Image", "user")
        insertMessage(user_id, answer, "system")

        return answer
    except Exception as e:
        return "Error!"

