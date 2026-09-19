def chunk_messages(
    messages: list[dict],
    max_chars: int = 20000
) -> list[str]:

    chunks = []
    current_chunk = []
    current_size = 0

    for message in messages:

        content = message["content"]

        if current_chunk and current_size + len(content) > max_chars:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_size = 0

        current_chunk.append(content)
        current_size += len(content)

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks