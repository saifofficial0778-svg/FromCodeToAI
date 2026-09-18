import re


def clean_text(text: str) -> str:

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove PDF date + title + page number
    text = re.sub(
        r"\d{2}/\d{2}/\d{4},\s*\d{1,2}:\d{2}\s+day-\S+\s*\d+/\d+",
        "",
        text
    )

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()