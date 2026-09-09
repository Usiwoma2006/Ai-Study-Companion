"""
Research agent service.

Tries to answer from retrieved_context (the student's own notes) first. If
the model signals the notes don't cover the question (NOT_IN_NOTES sentinel),
automatically searches the web via Tavily and answers from those results
instead — no student confirmation step. The final answer is clearly labeled
when it came from the web, and web citations are tagged distinctly ([Web: ...])
so they're never confused with note citations ([Document — Section, p.X]).
"""

import logging
import os

import cohere
from tavily import TavilyClient

from django.conf import settings

logger = logging.getLogger(__name__)

MODEL = "command-a-plus-05-2026"
HISTORY_TURN_CAP = 10
NOT_IN_NOTES_SENTINEL = "NOT_IN_NOTES"
WEB_LABEL_PREFIX = "Answer not from your notes:\n\n"

client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
_tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def _extract_text(response) -> str:
    text_parts = [
        block.text
        for block in response.message.content
        if getattr(block, "type", None) == "text"
    ]
    return "".join(text_parts).strip()


def _cap_history(chat_history: list[dict[str, str]]) -> list[dict[str, str]]:
    if not chat_history:
        return []
    return chat_history[-HISTORY_TURN_CAP:]

def _cap_history(chat_history: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep only the last HISTORY_TURN_CAP turns."""
    if not chat_history:
        return []
    return chat_history[-HISTORY_TURN_CAP:]


def _rewrite_query(query: str, capped_history: list[dict[str, str]]) -> str:
    """Rewrite a possibly-fragmentary follow-up query into a standalone query,
    using recent chat history for context. If there's no history, or the
    rewrite fails, fall back to the original query untouched.
    """
    if not capped_history:
        return query

    history_text = "\n".join(
        f"{turn.get('role', 'user')}: {turn.get('content', '')}"
        for turn in capped_history
    )

    rewrite_prompt = (
        "Given the conversation history and the latest user message, rewrite "
        "the latest message into a standalone question that makes sense "
        "without the history. If it is already standalone, return it "
        "unchanged. Return ONLY the rewritten question, nothing else.\n\n"
        f"Conversation history:\n{history_text}\n\n"
        f"Latest message: {query}\n\n"
        "Rewritten standalone question:"
    )

    try:
        response = client.chat(
            model=MODEL,
            messages=[{"role": "user", "content": rewrite_prompt}],
        )
        rewritten = _extract_text(response)
        return rewritten if rewritten else query
    except Exception:
        logger.exception("Query rewrite failed, falling back to original query")
        return query


def _format_context(retrieved_context: list[dict]) -> str:
    if not retrieved_context:
        return "No retrieved context available."

    formatted_chunks = []
    for chunk in retrieved_context:
        citation = f"[{chunk.get('document_title', 'Unknown document')}"
        if chunk.get("section_title"):
            citation += f" — {chunk['section_title']}"
        if chunk.get("page_number") is not None:
            citation += f", p.{chunk['page_number']}"
        citation += "]"
        formatted_chunks.append(f"{citation}\n{chunk.get('content', '')}")

    return "\n\n".join(formatted_chunks)


def _format_web_results(results: list[dict]) -> str:
    """Format Tavily results with [Web: ...] tags — visually distinct from
    note citations so students always know when an answer left their notes."""
    if not results:
        return "No web results available."

    formatted_chunks = []
    for result in results:
        title = result.get("title", "Untitled")
        url = result.get("url", "")
        citation = f"[Web: {title} — {url}]"
        content = result.get("content", "")
        formatted_chunks.append(f"{citation}\n{content}")

    return "\n\n".join(formatted_chunks)


def _build_notes_prompt(
    query: str,
    formatted_context: str,
    capped_history: list[dict[str, str]],
) -> list[dict[str, str]]:
    system_instructions = (
        "You are a research assistant. Synthesize an answer by drawing "
        "connections across the provided context chunks, which may come "
        "from multiple documents or sections. Explicitly note points of "
        "agreement, contradiction, or complementary detail across sources. "
        "Cite every claim using the bracketed source tags. "
        f"If the context does NOT contain enough information to answer the "
        f"question, respond with EXACTLY the single word "
        f"{NOT_IN_NOTES_SENTINEL} and nothing else — no explanation, no "
        f"partial answer."
    )

    messages = [{"role": "system", "content": system_instructions}]

    for turn in capped_history:
        role = "assistant" if turn.get("role") == "assistant" else "user"
        messages.append({"role": role, "content": turn.get("content", "")})

    user_turn = f"Context:\n{formatted_context}\n\nQuestion: {query}"
    messages.append({"role": "user", "content": user_turn})

    return messages


def _build_web_prompt(
    query: str,
    formatted_web_results: str,
    capped_history: list[dict[str, str]],
) -> list[dict[str, str]]:
    system_instructions = (
        "You are a research assistant. The student's own notes did not "
        "cover this question, so you're answering using web search results "
        "instead. Synthesize an answer from the provided web results, "
        "noting agreement, contradiction, or complementary detail across "
        "sources where relevant. Cite every claim using the bracketed "
        "[Web: ...] source tags provided."
    )

    messages = [{"role": "system", "content": system_instructions}]

    for turn in capped_history:
        role = "assistant" if turn.get("role") == "assistant" else "user"
        messages.append({"role": role, "content": turn.get("content", "")})

    user_turn = f"Web results:\n{formatted_web_results}\n\nQuestion: {query}"
    messages.append({"role": "user", "content": user_turn})

    return messages


def _web_search(query: str, max_results: int = 5) -> list[dict]:
    """Calls Tavily and returns results in a shape compatible with
    _format_web_results: title, url, content."""
    try:
        response = _tavily_client.search(query=query, max_results=max_results)
        return response.get("results", [])
    except Exception:
        logger.exception("Tavily web search failed for query: %s", query)
        return []


def run_research(
    query: str,
    chat_history: list[dict[str, str]],
    retrieved_context: list[dict],
) -> str:
    capped_history = _cap_history(chat_history)
    standalone_query = _rewrite_query(query, capped_history)

    # --- Phase 1: try answering from the student's own notes ---
    formatted_context = _format_context(retrieved_context)
    notes_messages = _build_notes_prompt(standalone_query, formatted_context, capped_history)

    try:
        response = client.chat(model=MODEL, messages=notes_messages)
        notes_answer = _extract_text(response)
    except Exception:
        logger.exception("Research agent LLM call (notes phase) failed")
        return "I ran into an error trying to research that. Please try again."

    if not notes_answer:
        logger.error("Research agent received empty text response (notes phase)")
        return "I wasn't able to produce a research synthesis for that. Please try rephrasing."

    if notes_answer.strip() != NOT_IN_NOTES_SENTINEL:
        # Notes were sufficient — return as-is, no web search needed.
        return notes_answer

    # --- Phase 2: notes were insufficient, search the web automatically ---
    logger.info("Research agent: notes insufficient, searching web for: %s", query)
    web_results = _web_search(query)

    if not web_results:
        return (
            "This isn't covered in your notes, and I wasn't able to find "
            "anything useful on the web for it either."
        )

    formatted_web_results = _format_web_results(web_results)
    web_messages = _build_web_prompt(standalone_query, formatted_web_results, capped_history)

    try:
        response = client.chat(model=MODEL, messages=web_messages)
        web_answer = _extract_text(response)
    except Exception:
        logger.exception("Research agent LLM call (web phase) failed")
        return "This isn't covered in your notes, and I ran into an error searching the web. Please try again."

    if not web_answer:
        logger.error("Research agent received empty text response (web phase)")
        return "This isn't covered in your notes, and I couldn't generate an answer from web results."

    return WEB_LABEL_PREFIX + web_answer