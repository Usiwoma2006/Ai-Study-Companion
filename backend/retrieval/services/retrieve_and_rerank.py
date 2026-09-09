from retrieval.services.hybrid_retrieval import hybrid_retrieval
from retrieval.services.reranker import rerank

def retrieve_and_rerank(query: str, notebook_id: int, top_k: int = 5, overfetch_multiplier: int = 3) -> list[dict]:
    candidates = hybrid_retrieval(query, notebook_id, top_k=top_k * overfetch_multiplier)
    return rerank(query, candidates, top_k=top_k)