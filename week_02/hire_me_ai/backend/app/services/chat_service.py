from app.clients.groq_client import client
from app.core.config import GROQ_MODEL
from app.schemas.resume import Resume

def ask_candidate(question: str, resume: Resume) -> str:

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
"""

    response = client.chat.completions.create(
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
        ]
    )

    return response.choices[0].message.content