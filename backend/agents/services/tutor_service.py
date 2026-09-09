"""
Tutor agent service.

Responsibilities:
1. Rewrite the incoming query into a standalone query using recent chat history
   (handles follow-ups like "the blue one" -> "I need a blue car").
2. Build a citation-aware prompt from retrieved_context + capped chat history.
3. Call Cohere ClientV2 (command-a-plus-05-2026), filter for text blocks only.
4. Return a plain string explanation.

NOTE: Query rewriting is implemented here (inside the Tutor agent) as a first
pass. Architecturally this probably belongs upstream — before routing/retrieval
— so that every agent (not just Tutor) benefits from a clean, standalone query.
Revisit this once a second agent needs the same behavior.
"""

import logging
import os

import cohere

from django.conf import settings

logger = logging.getLogger(__name__)

MODEL = "command-a-plus-05-2026"
HISTORY_TURN_CAP = 10  # last N turns folded into prompts (cost/context control)

client = cohere.ClientV2(api_key=os.getenv('COHERE_API_KEY'))


def _extract_text(response) -> str:
    """Cohere command-a-plus returns both 'text' and 'thinking' blocks.
    Only 'text' blocks are the actual answer."""
    text_parts = [
        block.text
        for block in response.message.content
        if getattr(block, "type", None) == "text"
    ]
    return "".join(text_parts).strip()


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
    """Format retrieved chunks with citation metadata for the prompt."""
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


def _build_prompt(
    standalone_query: str,
    formatted_context: str,
    capped_history: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Build the multi-turn message list for the tutor call."""
    system_instructions = (
        "You are a patient, clear tutor helping a student understand material "
        "from their notes. Use the provided context to explain concepts "
        "accurately. When you rely on a specific fact from the context, cite "
        "it inline using the bracketed citation shown with that excerpt "
        "(e.g. [Document Title — Section, p.4]). If the context doesn't "
        "contain enough information to answer confidently, say so plainly "
        "rather than guessing."
    )

    messages = [{"role": "system", "content": system_instructions}]

    # Fold in capped prior turns for conversational continuity
    for turn in capped_history:
        role = turn.get("role", "user")
        role = "assistant" if role == "assistant" else "user"
        messages.append({"role": role, "content": turn.get("content", "")})

    user_turn = (
        f"Context:\n{formatted_context}\n\n"
        f"Question: {standalone_query}"
    )
    messages.append({"role": "user", "content": user_turn})

    return messages


def run_tutor(
    query: str,
    chat_history: list[dict[str, str]],
    retrieved_context: list[dict],
) -> str:
    """Main entry point for the Tutor agent. Returns a plain string explanation."""
    capped_history = _cap_history(chat_history)
    standalone_query = _rewrite_query(query, capped_history)

    formatted_context = _format_context(retrieved_context)
    messages = _build_prompt(standalone_query, formatted_context, capped_history)

    try:
        response = client.chat(model=MODEL, messages=messages)
        answer = _extract_text(response)
    except Exception:
        logger.exception("Tutor agent LLM call failed")
        return (
            "I ran into an error trying to generate an explanation. "
            "Please try again."
        )

    if not answer:
        logger.error("Tutor agent received empty text response from model")
        return "I wasn't able to generate an explanation for that. Please try rephrasing."

    return answer