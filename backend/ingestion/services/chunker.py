def chunk_text(text, chunk_size=500, overlap=100):
    if not text or not text.strip():
        return []

    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def chunk_pages(
    pages_data: list[dict],
    chunk_size: int = 500,
    overlap: int = 100
) -> list[dict]:

    result = []
    global_chunk_index = 0

    for page in pages_data:
        text = page["text"].strip()

        if not text:
            continue

        section_title = page.get("section_title", "")

        text_chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk in text_chunks:
            result.append({
                "page_number": page["page_number"],
                "section_title": section_title,
                "content": chunk,
                "chunk_index": global_chunk_index,
            })

            global_chunk_index += 1

    return result