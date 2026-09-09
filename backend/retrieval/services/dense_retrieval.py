import os
import cohere

from pgvector.django import CosineDistance
from notebooks.models import Chunk

client = cohere.ClientV2(api_key=os.getenv('COHERE_API_KEY'))


def embed_query(query: str):
    response = client.embed(
        texts=[query],
        model='embed-english-v3.0',
        input_type='search_query',
        embedding_types=['float'],
    )
    return response.embeddings.float[0]


def dense_retrieval(query: str, notebook_id: int, top_k: int = 5):
    query_embedding = embed_query(query)

    chunks = (
        Chunk.objects
        .select_related("document")
        .filter(notebook_id=notebook_id)
        .annotate(distance=CosineDistance("embedding", query_embedding))
        .order_by("distance")[:top_k]   
    )

    results = []
    for chunk in chunks:
        results.append({
            "content" : chunk.content, 
            "page_number" : chunk.page_number, 
            "document_id" : chunk.document_id, 
            "document_title" : chunk.document.title,
            "section_title" : chunk.section_title, 
            "score": 1 - chunk.distance,
            "chunk_id": chunk.id,  
        })

    return results