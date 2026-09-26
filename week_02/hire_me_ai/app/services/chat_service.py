from app.clients.groq_client import client
from app.core.config import GROQ_MODEL
from app.schemas.resume import Resume

def ask_candidate(question: str, resume: Resume):

    system_prompt = f"""
You are an AI assistant representing a job candidate.

Below is the candidate's resume information:

{resume.model_dump_json(indent=2)}

Rules:

1. Answer only using the information provided in the resume.

2. Never invent or assume information.

3. If the information is not available, say:
"I don't have enough information to answer that."

4. Be professional and concise.

5. Answer as if HR is interviewing the candidate.

6. Keep answers short by default (2-4 sentences). Only give a longer,
detailed answer if the question explicitly asks for details, a full
list, or an in-depth explanation.
"""

    stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta