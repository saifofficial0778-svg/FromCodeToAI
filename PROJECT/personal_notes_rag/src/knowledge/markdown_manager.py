from pathlib import Path
from datetime import date

NOTES_DIR = Path("data/notes")


def update_note(topic: str, new_knowledge: str, source: str) -> Path:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    file_path = NOTES_DIR / f"{topic}.md"

    marker = f"<!-- source: {source} -->"

    # Same PDF dubara run kiya toh duplicate append nahi hoga
    if file_path.exists() and marker in file_path.read_text(encoding="utf-8"):
        print(f"⚠️ {source} already added, skipping.")
        return file_path

    block = f"\n\n{marker}\n<!-- added: {date.today()} -->\n\n{new_knowledge.strip()}\n"

    with file_path.open("a", encoding="utf-8") as f:
        f.write(block)

    return file_path