import re

WRAP_MIN = 100                       # PDF line ~130 char pe wrap hoti hai; isse chhoti line = paragraph end
SENT_END = (".", "!", "?", ":")

EMOJI = r"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]"
EMOJI_TAIL = re.compile(EMOJI + r"\s*$")
LIST_START = re.compile(r"^(\d+\.|[-•*])\s")

# ---------- config (apne chat ke hisaab se badalna) ----------
ACK_WORDS = {"bro", "broo", "bhai", "ok", "okay", "next", "done", "got", "it",
             "clear", "hai", "ho", "gya", "gaya", "chal", "hua"}
SKIP_TURN = re.compile(r"\bnotes do\b|khtm hua|khatam hua", re.I)   # user msg + uska reply dono drop
DROP_FIRST_USER = True

OPENERS = [
    r"^(arey|waah|wah|superb|bilkul|oh bhai|haan bhai|shabash)\b",
    r"^koi baat nahi",
    r"^chal(o)?\b",
    r"^ekdum sahi",
    r"^bhai,? (dil se )?(sorry|fikar)",
]
CLOSERS = [
    r"\bDone\b.*\b(bolo|likho|bol|bolna)\b|\b(bolo|likho|bol|bolna)\b.*\bDone\b",
    r"^(ab )?bata(o|na)?\b",
    r"^mujhe (batao|bata)\b",
    r"^dil se batana",
    r"^ki kaise\b.*\?$",
    r"^aaj ke liye\b.*\?$",
    r"\b(samajh aaya|clear hua|clear hai)\b.*\?$",
    r"^(kya bolte|kya bolti)",
    r"^all the best",
    r"^clear bolna\b",
    r"^(hamein aaj ke saare|aaj ka day)\b",
    r"^kal ko agar interviewer\b",
    r"\bsheet me agla point\b",
    r"^[\W_]+$",                     # sirf emoji/punctuation bacha ho
    r"(?=.*\bbhai\b)(?=.*\b(clear|samajh|dimaag|picture|doubt|makkhan|daccan|fit)\b).*\?\s*$",
]
META = re.compile(r"Screenshot \d{4}-\d{2}-\d{2}.*?\.png")   # kisi bhi jagah ka meta-sentence

# ---------- code detection ----------
CODE_PATTERNS = [re.compile(p) for p in (
    r"^\s*//",
    r"^\s*(const|let|var)\s+\w+\s*=",
    r"^\s*function\s*\w*\s*\(",
    r"^\s*\(function",
    r"^\s*(for|if|while)\s*\(",
    r"^\s*console\.\w+\(",
    r"^\s*[})\]]+[;,)]*\s*$",
    r"^\s*\w+\s*:\s*function\s*\(",
    r"[;{}]\s*(//.*)?$",
)]


def is_code_line(line: str) -> bool:
    return any(p.search(line) for p in CODE_PATTERNS)


def heading_level(line: str) -> int:
    s = line.strip()
    if len(s) > 90 or "!" in s:
        return 0
    if re.match(r"^(Topic|Question) \d", s):
        return 1
    if re.match(r"^Scenario \d", s):
        return 2
    if EMOJI_TAIL.search(s) and len(s.split()) <= 12:
        return 2
    return 0


def clean_title(s: str) -> str:
    return re.sub(EMOJI + "+", "", s).strip()


# ---------- text -> blocks ----------
def to_blocks(text: str) -> list[tuple[str, str]]:
    """(kind, text): kind = h1 | h2 | prose | code"""
    blocks, para, code = [], [], []

    def flush_para():
        if para:
            blocks.append(("prose", " ".join(para)))
            para.clear()

    def flush_code():
        while code and not code[-1].strip():
            code.pop()
        if code:
            blocks.append(("code", "\n".join(code)))
            code.clear()

    for line in text.split("\n"):
        stripped = line.strip()

        if code:
            if not stripped or line.startswith(" ") or is_code_line(line):
                code.append(line.rstrip())
                continue
            flush_code()

        if not stripped:
            flush_para()
            continue

        if is_code_line(line):
            flush_para()
            code.append(line.rstrip())
            continue

        lvl = heading_level(line)
        if lvl:
            flush_para()
            blocks.append((f"h{lvl}", stripped))
            continue

        if LIST_START.match(stripped):
            flush_para()

        para.append(stripped)
        # lambi line jo sentence pe khatam nahi hui = wrap hui hai, agli line se jodo
        if len(stripped) < WRAP_MIN or stripped.endswith(SENT_END):
            flush_para()

    flush_para()
    flush_code()
    return blocks


# ---------- noise rules ----------
def split_sentences(p: str) -> list[str]:
    # ." / ?" jaise quote-closing ke baad bhi sentence todo (IIFE answer wala bug fix)
    return re.split(r'(?<=[.!?])\s+|(?<=[.!?]["”])\s+', p.strip())


def matches(sentence: str, patterns: list[str]) -> bool:
    return any(re.search(p, sentence, re.I) for p in patterns)


def strip_edges(blocks, patterns, from_end: bool, removed: list[str]):
    idx = -1 if from_end else 0
    while blocks and blocks[idx][0] == "prose":
        sents = split_sentences(blocks[idx][1])
        pick = (lambda: sents[-1]) if from_end else (lambda: sents[0])
        pop = (lambda: sents.pop()) if from_end else (lambda: sents.pop(0))
        while sents and len(pick()) < 250 and matches(pick(), patterns):
            removed.append(pop())
        if sents:
            blocks[idx] = ("prose", " ".join(sents))
            break
        blocks.pop(idx)
    return blocks


def drop_meta(blocks, removed):
    out = []
    for kind, body in blocks:
        if kind == "prose":
            sents = split_sentences(body)
            removed += [s for s in sents if META.search(s)]
            sents = [s for s in sents if not META.search(s)]
            if not sents:
                continue
            body = " ".join(sents)
        out.append((kind, body))
    return out


def is_ack(text: str) -> bool:
    words = re.findall(r"[a-z0-9%]+", text.lower())
    return all(w in ACK_WORDS or re.fullmatch(r"\d+%?", w) for w in words)


# ---------- messages -> sections ----------
def is_filler_section(s) -> bool:
    text = " ".join(b for _, b in s["blocks"])
    has_code = any(k == "code" for k, _ in s["blocks"])
    return s["heading"] == "Notes" and not has_code and len(text) < 600


def structure_chat(messages: list[dict]):
    sections, removed = [], []
    topic, current, skip_reply = "General", None, False

    def new_section(heading):
        sec = {"topic": topic, "heading": heading, "blocks": []}
        sections.append(sec)
        return sec

    for i, m in enumerate(messages):
        role, text = m["role"], m["content"]

        if role == "user":
            skip_reply = bool(SKIP_TURN.search(text))
            if (DROP_FIRST_USER and i == 0) or skip_reply or is_ack(text):
                removed.append(f"[user] {text}")
                current = None
                continue
            short = re.sub(r"\s+", " ", text)[:70]
            current = new_section("Doubt: " + short)
            current["blocks"].append(("prose", f"Q: {text}"))
            continue

        if skip_reply:
            removed.append(f"[assistant, skipped turn] {text[:120]}...")
            skip_reply, current = False, None
            continue

        blocks = to_blocks(text)
        blocks = drop_meta(blocks, removed)
        blocks = strip_edges(blocks, OPENERS, from_end=False, removed=removed)
        blocks = strip_edges(blocks, CLOSERS, from_end=True, removed=removed)

        for kind, body in blocks:
            if kind in ("h1", "h2"):
                title = clean_title(body)
                if kind == "h1":
                    topic = title
                current = new_section(title)
            else:
                if current is None:
                    current = new_section("Notes")
                current["blocks"].append((kind, body))
        current = None

    kept = []
    for s in sections:
        if not s["blocks"]:
            continue
        if is_filler_section(s):
            removed.append("[filler section] " + " ".join(b for _, b in s["blocks"])[:150])
        else:
            kept.append(s)
    return kept, removed


# ---------- output ----------
def render_blocks(blocks, lang="javascript") -> str:
    return "\n\n".join(
        f"```{lang}\n{b}\n```" if k == "code" else b for k, b in blocks
    )


def to_markdown(sections) -> str:
    out, last_topic = [], None
    for s in sections:
        if s["topic"] != last_topic:
            out.append(f"# {s['topic']}")
            last_topic = s["topic"]
        if s["heading"] != s["topic"]:
            out.append(f"## {s['heading']}")
        out.append(render_blocks(s["blocks"]))
    return "\n\n".join(out) + "\n"


def make_chunks(sections, source: str, max_chars=1800, min_chars=250) -> list[dict]:
    size = lambda blocks: sum(len(b) for _, b in blocks)
    parts = []

    for s in sections:                       # bade section ko blocks ki boundary pe todo
        cur = []
        for blk in s["blocks"]:
            if cur and size(cur) + len(blk[1]) > max_chars:
                parts.append({**s, "blocks": cur})
                cur = []
            cur.append(blk)
        if cur:
            parts.append({**s, "blocks": cur})

    merged = []                              # bahut chhote chunk ko pichle (same topic) me jodo
    for p in parts:
        if (merged and merged[-1]["topic"] == p["topic"]
                and size(p["blocks"]) < min_chars
                and size(merged[-1]["blocks"]) + size(p["blocks"]) <= max_chars * 1.3):
            merged[-1]["blocks"] += [("prose", f"{p['heading']}:")] + p["blocks"]
        else:
            merged.append(p)

    chunks = []
    for n, p in enumerate(merged):
        body = render_blocks(p["blocks"])
        chunks.append({
            "id": f"{source}:{n}",
            "source": source,
            "topic": p["topic"],
            "section": p["heading"],
            "has_code": any(k == "code" for k, _ in p["blocks"]),
            "text": f"## {p['heading']}\n\n{body}",
            "embed_text": f"{p['topic']} > {p['heading']}\n\n{body}",   # context header ke saath embed hoga
        })
    return chunks