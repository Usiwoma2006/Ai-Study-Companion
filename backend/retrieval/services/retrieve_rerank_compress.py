from retrieval.services.retrieve_and_rerank import retrieve_and_rerank
from retrieval.services.context_compressor import compress_context


def retrieve_rerank_compress(query: str, notebook_id: int, top_k: int = 5) -> list[dict]:
    results = retrieve_and_rerank(query, notebook_id, top_k=top_k)
    return compress_context(query, results)