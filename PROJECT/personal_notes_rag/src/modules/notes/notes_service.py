from pathlib import Path

from ingestion.pdf_loader import read_pdf
from ingestion.chat_parser import parse_chat
from cleaner.cleaner import clean_text
from cleaner.chunker import chunk_messages
from cleaner.llm_cleaner import clean_with_llm
from knowledge.markdown_manager import update_note


def import_notes(file_path: Path, topic: str):

    # PDF → raw text
    raw_text = read_pdf(file_path)

    # Raw text → messages
    messages = parse_chat(raw_text)

    # Rule cleaning
    cleaned_messages = []

    for message in messages:

        cleaned = clean_text(message["content"])

        if cleaned:
            cleaned_messages.append({
                "role": message["role"],
                "content": cleaned
            })

    # Create chunks
    chunks = chunk_messages(
        cleaned_messages,
        max_chars=20000
    )

    # LLM cleaning
    cleaned_parts = []

    for chunk in chunks:

        cleaned = clean_with_llm(chunk)

        if cleaned:
            cleaned_parts.append(cleaned)

    cleaned_knowledge = "\n\n".join(cleaned_parts)

    # Save / merge Markdown
    file_path = update_note(
        topic=topic,
        new_knowledge=cleaned_knowledge
    )

    return file_path