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
prompt1="hii"
prompt2="Explain time travel in detail under 100 words"
prompt3="write 1000 word essay on machine learning"

prompts=[prompt1,prompt2,prompt3]

for prompt in prompts:
    message = {
        "role": role,
        "content": prompt
    }
    


    messages = [message]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=5000
    )
    usage = response.usage
    print('----------------------------------------')
    print(f'Prompt: {prompt}-->your token: {usage.prompt_tokens}-->completion token: {usage.completion_tokens}-->total token: {usage.total_tokens} -->finish reason: {response.choices[0].finish_reason}')
