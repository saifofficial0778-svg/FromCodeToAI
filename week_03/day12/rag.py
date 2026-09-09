import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set. Please set it in your .env file."
    )
client = Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

#step1
knowledge_base={
    "age":"the age of the mohd saif is 23 years.",
    "net worth":"The net worth of the mohd saif is 1.5 million dollars.",
    "birth year":"Mohd Saif was born in 2003."
}

def retrieve_answer(question):
    question_lower = question.lower()
    for key in knowledge_base:
        if key in question_lower:
            return knowledge_base[key]
    return "I don't know the answer to that question."

def ask_llm(question):
    context = retrieve_answer(question)
    sys_prompt = f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""

    system_message = {
        "role": "system",
        "content": sys_prompt
    }

    message = {
        "role": "user",
        "content": question
    }

    messages = [system_message, message]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    ans = response.choices[0].message.content
    return ans

print(ask_llm("birthhhh year of mohd saif?"))
    