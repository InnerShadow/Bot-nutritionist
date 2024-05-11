from openai import OpenAI
from PIL import Image
import base64

from DataBaseHeplers.getUsersData import get_users_data
from DataBaseHeplers.getMessageHistory import getMessageHistory
from DataBaseHeplers.insertMessage import insertMessage

# Function to encode image to OPEN AI AIP
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

# If image too huge, just squeeze it by half
def reduce_image_quality(image_path):
    img = Image.open(image_path)
    img = img.resize((img.size[0] // 2, img.size[1] // 2))
    img.save(image_path)


# Function to generate response based on image input
def generate_photo_response(token : str, photo : str, user_id : int, caption : str) -> str:
    client = OpenAI(api_key = token)

    # Use try/catch block to track OPEN AI API errors
    try:
        # Get 10 prev messages
        user_data = get_users_data(user_id)

        # Say that we need nutritionist specialist
        history = []
        history.append({
                        'role' : "system", 
                        "content" : "You are nutritionist specialist. Aswer only questions from you're scope of knowledge."
                    })
        
        # Say besed information about user
        history.append({
                        'role' : "user", 
                        "content" : f"""My name is {user_data[5]}, i am {user_data[2]}, i am {user_data[8]} years old,
                                        my hight is {user_data[3]} cm, my weight is {user_data[4]} kg, i ask question for \"{user_data[6]}\", 
                                        my diet is : \"{user_data[9]}\". Call me by my first name and use this information about my health condition in the response."""
                        })

        # And append all prev messages
        for mesg, role in reversed(getMessageHistory(user_id)):
            history.append({'role': role, 'content': mesg})

        # Preprocess image and squeeze it by half if it too huge
        # cause OPEN AI has limit into 124 000 tokens to preprocess
        base64_image = encode_image(photo)
        while len(base64_image) > 86_000:
            reduce_image_quality(photo)
            base64_image = encode_image(photo)
        
        # Generate response
        response = client.chat.completions.create(

            # Chhose vision model to preprocess images
            model = "gpt-4-vision-preview",
            messages = history + [
                {
                    "role": "user",

                    # Write promt to cout proteins\fats\carbohydrates and calorie from photo
                    "content": [
                        {
                            "type": "text", 
                            "text": f"""Predict number of the proteins\\fats\\carbohydrates and calorie content on image. " + caption + ".
                                        In your reply, use the language from the previous correspondence. And: \" {caption}\"."""},

                        # And send preprocess image
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ]
        )

        # Preprocess answer
        answer = response.choices[0].message.content.replace("*", "").replace("#", "")

        # Save images into database
        insertMessage(user_id, "Image", "user")
        insertMessage(user_id, answer, "system")

        return answer
    except Exception as e:
        return "Error!"

