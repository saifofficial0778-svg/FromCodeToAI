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
prompt = "how internet work? write a essay in 1000 words"

message = {
    "role": role,
    "content": prompt
}

messages = [message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True
)

for chunk in response:
    content=chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)