import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"
MAX_NOISE_RATIO = 0.6          # isse zyada delete karna ho toh kuch gadbad hai
LOG_PATH = Path("data/logs/removed.txt")

SYSTEM_PROMPT = """
You will get numbered pieces from a Hinglish learning chat.
Return the IDs of pieces that are PURE conversational noise:
greetings, praise, motivation, "Done bolo / next chalte hain" type lines,
"ab clear hua?" type check-in questions, apologies, jokes with no concept.

If a piece has ANY learning content (explanation, analogy, example, code,
interview answer, definition, a concept question), it is NOT noise.
If unsure, it is NOT noise.

Return ONLY JSON, nothing else: {"noise": [3, 7]}
Return {"noise": []} if nothing is noise.
"""


def is_code(piece: str) -> bool:
    if piece.lstrip().startswith("```"):
        return True
    lines = [l.strip() for l in piece.splitlines() if l.strip()]
    if not lines:
        return False
    codey = sum(
        l.endswith((";", "{", "}", ")")) or l.startswith(("//", "console."))
        for l in lines
    )
    return codey / len(lines) > 0.6


def ask_llm_for_noise_ids(listing: str, n_pieces: int) -> set[int]:
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": listing},
                ],
                temperature=0,
                reasoning_effort="low",   # thinking tokens kam; Groq docs me param check kar lena
            )
            content = resp.choices[0].message.content
            match = re.search(r"\{.*\}", content, re.DOTALL)
            data = json.loads(match.group(0))
            return {int(i) for i in data["noise"] if 0 <= int(i) < n_pieces}

        except Exception as error:
            if "429" in str(error):
                print("   ⏳ Rate limit, waiting 12s...")
                time.sleep(12)
            else:
                print(f"   ⚠️ LLM/JSON failed: {error}")
                break

    return set()   # fail hua toh kuch delete nahi hoga


def clean_with_llm(text: str) -> str:
    pieces = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    listing = "\n\n".join(f"[{i}] {p}" for i, p in enumerate(pieces))

    noise = ask_llm_for_noise_ids(listing, len(pieces))

    # code ko kabhi delete mat karo
    noise = {i for i in noise if not is_code(pieces[i])}

    # safety guard
    if pieces and len(noise) / len(pieces) > MAX_NOISE_RATIO:
        print(f"   ⚠️ {len(noise)}/{len(pieces)} pieces noise bole, suspicious. Keeping all.")
        noise = set()

    # audit log
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        for i in sorted(noise):
            f.write(f"--- removed ---\n{pieces[i]}\n\n")

    return "\n\n".join(p for i, p in enumerate(pieces) if i not in noise)