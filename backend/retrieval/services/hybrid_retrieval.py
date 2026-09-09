from retrieval.services.dense_retrieval import dense_retrieval
from retrieval.services.sparse_retrieval import sparse_retrieval

def hybrid_retrieval(query: str, notebook_id: int, top_k: int = 5) -> list[dict]:
    dense_results = dense_retrieval(query, notebook_id, top_k=top_k * 2)
    sparse_results = sparse_retrieval(query, notebook_id, top_k=top_k * 2)

    k = 60
    scores = {}
    chunk_data = {}

    for rank, r in enumerate(dense_results, 1):
        scores[r["chunk_id"]] = scores.get(r["chunk_id"], 0) + 1 / (k + rank)
        chunk_data[r["chunk_id"]] = r

    for rank, r in enumerate(sparse_results, 1):
        scores[r["chunk_id"]] = scores.get(r["chunk_id"], 0) + 1 / (k + rank)
        chunk_data.setdefault(r["chunk_id"], r)

    sorted_ids = sorted(scores, key=scores.get, reverse=True)[:top_k]

    results = []
    for cid in sorted_ids:
        result = dict(chunk_data[cid])
        result["score"] = scores[cid]
        results.append(result)

    return results