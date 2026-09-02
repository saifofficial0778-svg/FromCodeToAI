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
prompt = "suggest a name for my food company"
#system message to set the context of the conversation
message_system = {
    "role":"system",
    "content":"You are my brand manager who suggests name for my food company. name should be in one word suggest one name only"
}

message = {
    "role": role,
    "content": prompt
}

messages = [message_system, message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=1,
)
print('----------------------------------------')
print('----------------------------------------')
print(response.choices[0].message.content)