import os
import cohere

client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))


def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    if not candidates:
        return []

    response = client.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=[c["content"] for c in candidates],
        top_n=top_k,
    )

    results = []
    for r in response.results:
        candidate = candidates[r.index]
        candidate["rerank_score"] = r.relevance_score
        results.append(candidate)

    return results