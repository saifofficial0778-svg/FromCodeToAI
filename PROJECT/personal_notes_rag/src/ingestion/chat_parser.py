import re


def parse_chat(text: str) -> list[dict]:
    pattern = r"(User prompt:|Response:)(.*?)(?=User prompt:|Response:|\Z)"

    matches = re.findall(pattern, text, re.DOTALL)

    messages = []

    for role, content in matches:
        content = content.strip()

        if not content:
            continue

        messages.append({
            "role": "user" if role == "User prompt:" else "assistant",
            "content": content
        })

    return messages