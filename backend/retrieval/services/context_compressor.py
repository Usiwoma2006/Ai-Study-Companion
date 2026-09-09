import os
import json
import cohere

client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))


def compress_context(query: str, results: list[dict]) -> list[dict]:
    if not results:
        return []

    chunks_text = "\n\n".join(
        f"chunk_id: {r['chunk_id']}\ncontent: {r['content']}"
        for r in results
    )
    prompt = (
        f'Given the query: "{query}"\n\n'
        "For each chunk below, extract only the sentences relevant "
        "to answering the query. If nothing in a chunk is relevant, "
        "return an empty string for it.\n\n"
        f"{chunks_text}\n\n"
        "Respond ONLY with valid JSON. Use the EXACT chunk_id values shown above as the keys "
        '(e.g. if a chunk above has "chunk_id: 42", the key should be "42", not a placeholder). '
        "Example format:\n"
        '{"42": "relevant text here", "17": "relevant text here"}'
    )

    response = client.chat(
        model="command-a-plus-05-2026",
        messages=[{"role": "user", "content": prompt}],
    )

    # response.message.content is a list of content blocks (may include
    # a 'thinking' block before the actual 'text' block) — find the text one
    raw_text = next(
        (item.text for item in response.message.content if item.type == "text"),
        "",
    )

    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        compressed_map = json.loads(cleaned)
    except json.JSONDecodeError:
        compressed_map = {}

    for r in results:
        r["content"] = compressed_map.get(str(r["chunk_id"]), r["content"])

    return results