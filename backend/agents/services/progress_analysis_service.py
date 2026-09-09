"""
Progress analysis agent service.

Analyzes chat_history (and, where relevant, retrieved_context) to surface
patterns in the student's learning — recurring struggle areas, topics
revisited multiple times, apparent gaps. Returns a plain string analysis.
"""

import logging
import os

import cohere

from django.conf import settings

logger = logging.getLogger(__name__)

MODEL = "command-a-plus-05-2026"
HISTORY_TURN_CAP = 10

client = cohere.ClientV2(api_key=os.getenv('COHERE_API_KEY'))


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


def _build_prompt(
    query: str,
    formatted_context: str,
    capped_history: list[dict[str, str]],
    quiz_summary: str,
) -> list[dict[str, str]]:
    system_instructions = (
        "You are a learning progress analyst. Review the conversation "
        "history and quiz performance summary for patterns — topics the "
        "student has asked about repeatedly, signs of confusion, or areas "
        "with weak quiz performance. Use the provided context only to "
        "ground any topic references. If there isn't enough information to "
        "draw meaningful conclusions, say so plainly."
    )

    messages = [{"role": "system", "content": system_instructions}]

    for turn in capped_history:
        role = "assistant" if turn.get("role") == "assistant" else "user"
        messages.append({"role": role, "content": turn.get("content", "")})

    user_turn = (
        f"Context:\n{formatted_context}\n\n"
        f"Quiz performance:\n{quiz_summary}\n\n"
        f"Request: {query}"
    )
    messages.append({"role": "user", "content": user_turn})

    return messages


def run_progress_analysis(
    query: str,
    chat_history: list[dict[str, str]],
    retrieved_context: list[dict],
    quiz_summary: str,
) -> str:
    capped_history = _cap_history(chat_history)
    formatted_context = _format_context(retrieved_context)
    messages = _build_prompt(query, formatted_context, capped_history, quiz_summary)

    try:
        response = client.chat(model=MODEL, messages=messages)
        answer = _extract_text(response)
    except Exception:
        logger.exception("Progress analysis agent LLM call failed")
        return "I ran into an error trying to analyze progress. Please try again."

    if not answer:
        logger.error("Progress analysis agent received empty text response")
        return "I wasn't able to produce a progress analysis. Please try rephrasing."

    return answer

  