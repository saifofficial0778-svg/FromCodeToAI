import os
from dotenv import load_dotenv
from groq import Groq
import base64

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set. Please set it in your .env file."
    )

client = Groq(api_key=my_api_key)

model="qwen/qwen3.6-27b"
  
    
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
image_path = "Graduation_Marksheet.jpg"

base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts information from images and text. in JSON format only. Do not provide any explanation or additional text. Only provide the JSON output."
        },
        {
            "role": "user",
            "content": [
                
                {
                    "type": "text",
                    "text": "one the basis of this marksheet can we hire this candiadte or not ans is depend on u"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"""data:image/jpeg;base64,{base64_image}"""
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)