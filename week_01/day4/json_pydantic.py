import os
from pydoc import text
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

from pydantic import BaseModel
class Ticket(BaseModel):
    name: str
    product: str
    issue: str
    email: str
    request: str

schema = Ticket.model_json_schema()
response_format = {
    "type": "json_object"
}

system_prompt = f"""You are a helpful assistant that extracts information from customer support tickets strictly based on this schema: {schema} and give it in JSON format."""

system_message = {
    "role": "system",
    "content": system_prompt
}

text="My name is Saif I purchased a new laptop from Amazon but it is not working properly. I want to return it and get a refund. Can you help me with the return process? my email is saif@example.com and my address is 123 Main Street, Cityville, State, 12345. I would like to return the laptop and receive a full refund. Please provide me with the necessary steps and any required documentation for the return process. Thank you."
prompt = f"""This is customer tiket: {text}. Please extract the following information:"""

message = {
    "role": role,
    "content": prompt
}

messages = [system_message, message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)

print(response.choices[0].message.content)