from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from notebooks.models import Chunk

def sparse_retrieval(query: str, notebook_id: int, top_k: int = 5):

    chunks = (
        Chunk.objects
        .select_related("document")
        .filter(notebook_id=notebook_id)
        .annotate(
        rank=SearchRank(SearchVector('content'), SearchQuery(query))
        )
        .order_by('-rank')[:top_k]  # note: higher rank = better, unlike distance where lower = better
    )


    results = []
    for chunk in chunks:
        results.append({
            "content" : chunk.content, 
            "page_number" : chunk.page_number, 
            "document_id" : chunk.document_id, 
            "document_title" : chunk.document.title,
            "section_title" : chunk.section_title, 
            "score": chunk.rank,
            "chunk_id": chunk.id,  
        })

    return results