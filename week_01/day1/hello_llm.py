import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set. Please set it in your .env file."
    )

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"

role = "user"
prompt = "2+2*2*6*5/8*6/2/9*94*59*5/5"

message = {
    "role": role,
    "content": prompt
}

messages = [message]

response = client.chat.completions.create(
    model=model,
    messages=messages
)

print(response.choices[0].message.content)