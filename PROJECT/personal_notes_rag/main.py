from pathlib import Path

from ingestion.pdf_loader import read_pdf
from ingestion.chat_parser import parse_chat
from cleaner.cleaner import clean_text
from cleaner.llm_cleaner import clean_with_llm
from knowledge.markdown_manager import update_note


PDF_PATH = Path("data/raw/day-09-closure.pdf")


# 1. PDF → raw text
raw_text = read_pdf(PDF_PATH)


# 2. Raw text → messages
messages = parse_chat(raw_text)


# 3. Rule cleaning
cleaned_messages = []

for message in messages:
    cleaned = clean_text(message["content"])

    if cleaned:
        cleaned_messages.append({
            "role": message["role"],
            "content": cleaned
        })


# 4. Messages → one text
chat_text = "\n\n".join(
    message["content"]
    for message in cleaned_messages
)


# 5. LLM noise removal
cleaned_knowledge = clean_with_llm(chat_text)


# 6. Save / merge into JavaScript notes
file_path = update_note(
    "javascript",
    cleaned_knowledge
)

print(f"\n✅ Notes updated: {file_path}")