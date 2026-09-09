import logging

from routing.services.heuristics import heuristic_route
from routing.services.llm_fallback import llm_route

logger = logging.getLogger(__name__)


def route_query(query: str) -> tuple[str, str]:
    """
    Entry point for query routing. Tries the heuristic layer first (cheap,
    no API call); falls through to the LLM classifier only when the
    heuristic can't confidently decide.

    Returns:
        (agent, method) — agent is one of the 5 valid labels, method is
        "heuristic", "llm_fallback", or "llm_fallback_error" (Cohere call
        itself failed, not just a bad/unparseable response — that case is
        already handled inside llm_route).
    """
    agent = heuristic_route(query)
    if agent is not None:
        logger.info("Routed via heuristic: %s -> %s", query, agent)
        return (agent, "heuristic")

    try:
        agent = llm_route(query)
        logger.info("Routed via llm_fallback: %s -> %s", query, agent)
        return (agent, "llm_fallback")
    except Exception:
        # Cohere call itself failed (network, auth, rate limit, etc.) —
        # llm_route already handles bad/unparseable *responses* internally,
        # this catches the call failing outright so a Cohere outage
        # doesn't crash the whole graph.
        logger.exception("llm_route raised an exception for query: %s", query)
        return ("tutor", "llm_fallback_error")