from pathlib import Path
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
client = Groq(api_key=GROQ_API_KEY)

NOTES_DIR = Path("data/notes")


MERGE_PROMPT = """
You are a strict Markdown knowledge merger.

You will receive:

1. EXISTING NOTE
2. NEW CLEANED KNOWLEDGE

Your job is to merge them into one Markdown note.

RULES:

- Preserve existing useful knowledge.
- Add only genuinely new knowledge.
- Remove duplicate information.
- Do NOT summarize.
- Do NOT rewrite existing sentences.
- Do NOT translate English/Hinglish.
- Do NOT correct grammar or spelling.
- Do NOT add outside knowledge.
- Preserve useful code exactly.
- Preserve useful examples exactly.
- Preserve interview points exactly.
- Keep the original English/Hinglish wording.
- Organize new knowledge under the appropriate existing topic heading.
- If a topic does not exist, create a new heading.
- Return ONLY the final Markdown.
"""


def merge_notes(existing_note: str, new_knowledge: str) -> str:

    prompt = f"""
    EXISTING NOTE:

    {existing_note}


    NEW CLEANED KNOWLEDGE:

    {new_knowledge}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": MERGE_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def update_note(topic: str, new_knowledge: str):

    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    file_path = NOTES_DIR / f"{topic}.md"

    if file_path.exists():

        existing_note = file_path.read_text(
            encoding="utf-8"
        )

        merged_note = merge_notes(
            existing_note,
            new_knowledge
        )

        file_path.write_text(
            merged_note,
            encoding="utf-8"
        )

    else:

        file_path.write_text(
            new_knowledge,
            encoding="utf-8"
        )

    return file_path