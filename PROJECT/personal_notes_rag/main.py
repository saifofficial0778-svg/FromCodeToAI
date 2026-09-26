import json
from pathlib import Path

from src.ingestion.pdf_loader import read_pdf
from src.ingestion.chat_parser import parse_chat
from src.cleaner.cleaner import clean_text
from src.cleaner.structurer import structure_chat, to_markdown, make_chunks

PDF_PATH = Path("data/raw/day-04-function.pdf")

raw_text = read_pdf(PDF_PATH)
messages = [
    {"role": m["role"], "content": clean_text(m["content"])}
    for m in parse_chat(raw_text)
]

sections, removed = structure_chat(messages)

# 1. Readable notes (per-day file, dobara run karo toh sirf ye file overwrite hogi)
md_path = Path("data/notes/javascript") / f"{PDF_PATH.stem}.md"
md_path.parent.mkdir(parents=True, exist_ok=True)
md_path.write_text(to_markdown(sections), encoding="utf-8")

# 2. Embedding ke liye chunks
chunks = make_chunks(sections, source=PDF_PATH.name)
chunks_path = Path("data/chunks") / f"{PDF_PATH.stem}.jsonl"
chunks_path.parent.mkdir(parents=True, exist_ok=True)
with chunks_path.open("w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

# 3. Audit
log = Path("data/logs/removed.txt")
log.parent.mkdir(parents=True, exist_ok=True)
log.write_text("\n---\n".join(removed), encoding="utf-8")

print(f"sections={len(sections)} chunks={len(chunks)} removed={len(removed)}")
print(f"notes: {md_path}\nchunks: {chunks_path}\nremoved: {log}")