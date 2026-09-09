"""
Study planner agent service.

Prioritizes study topics/actions based on retrieved_context and chat_history
(e.g. recently struggled-with topics, upcoming material). Returns a plain
string study plan.
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
) -> list[dict[str, str]]:
    system_instructions = (
        "You are a study planner. Using the provided context and the "
        "conversation history (which may reveal topics the student has "
        "struggled with or already covered), produce a prioritized, "
        "actionable study plan. Prefer concrete steps ('Review X, then "
        "practice Y') over vague advice. Cite context using the bracketed "
        "source tags where relevant. If there isn't enough information to "
        "build a plan, say so plainly and ask what topics to prioritize."
    )

    messages = [{"role": "system", "content": system_instructions}]

    for turn in capped_history:
        role = "assistant" if turn.get("role") == "assistant" else "user"
        messages.append({"role": role, "content": turn.get("content", "")})

    user_turn = f"Context:\n{formatted_context}\n\nRequest: {query}"
    messages.append({"role": "user", "content": user_turn})

    return messages


def run_study_planner(
    query: str,
    chat_history: list[dict[str, str]],
    retrieved_context: list[dict],
) -> str:
    capped_history = _cap_history(chat_history)
    formatted_context = _format_context(retrieved_context)
    messages = _build_prompt(query, formatted_context, capped_history)

    try:
        response = client.chat(model=MODEL, messages=messages)
        answer = _extract_text(response)
    except Exception:
        logger.exception("Study planner agent LLM call failed")
        return "I ran into an error trying to build a study plan. Please try again."

    if not answer:
        logger.error("Study planner agent received empty text response from model")
        return "I wasn't able to build a study plan for that. Please try rephrasing."

    return answer