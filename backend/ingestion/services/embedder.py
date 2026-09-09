import os
import cohere
from dotenv import load_dotenv

load_dotenv()

co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

EMBED_MODEL = "embed-english-v3.0"
BATCH_SIZE = 96  # Cohere's practical batch limit per request


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes chunk_pages() output, returns the same list with an
    'embedding' key added to each dict.
    """
    texts = [chunk["content"] for chunk in chunks]

    all_embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        response = co.embed(
            texts=batch,
            model=EMBED_MODEL,
            input_type="search_document",
            embedding_types=["float"],
        )
        all_embeddings.extend(response.embeddings.float)

    for chunk, embedding in zip(chunks, all_embeddings):
        chunk["embedding"] = embedding

    return chunks