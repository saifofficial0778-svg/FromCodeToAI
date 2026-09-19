from groq import Groq
import os
from dotenv import load_dotenv
import time

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
client = Groq(api_key=GROQ_API_KEY)


SYSTEM_PROMPT = """
You are a strict noise remover for personal learning notes.

Your job is ONLY to remove conversational noise from the given chat.

IMPORTANT RULES:

1. Preserve useful text EXACTLY as it appears.
2. Do NOT rewrite or rephrase sentences.
3. Do NOT summarize.
4. Do NOT translate English/Hinglish.
5. Do NOT correct grammar or spelling.
6. Do NOT add your own knowledge.
7. Preserve code EXACTLY.
8. Preserve useful examples EXACTLY.
9. Preserve technical explanations EXACTLY.
10. Preserve interview points EXACTLY.

Remove ONLY conversational/filler content such as:
- "bhai"
- "bro"
- "bilkul"
- "koi tension nahi"
- "chalo"
- "ab batao"
- "samajh aaya?"
- "done bolo"
- "next chalte hain"
- motivational talk
- greetings
- repeated conversational instructions
- unnecessary reactions/emojis

If a sentence contains both useful knowledge and conversational words,
remove ONLY the conversational part while preserving the useful text.

Return ONLY the cleaned text.
Do not explain what you removed.
"""


def clean_with_llm(text: str) -> str:

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=0
            )

            return response.choices[0].message.content.strip()

        except Exception as error:

            if "429" in str(error):

                wait_time = 12

                print(
                    f"   ⏳ Rate limit reached. "
                    f"Waiting {wait_time}s..."
                )

                time.sleep(wait_time)

            else:
                raise error

    raise RuntimeError(
        "LLM request failed after maximum retries."
    )