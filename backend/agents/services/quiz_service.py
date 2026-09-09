"""
Quiz agent service.

Generates quiz questions grounded in retrieved_context. Internally asks the
model for structured JSON (question, options, correct_answer, citation), then
formats it into a plain string for agent_output — consistent with the current
state contract (agent_output: str | None). Revisit once structured output is
supported in state.
"""

import json
import logging
import os

import cohere

from django.conf import settings

logger = logging.getLogger(__name__)

MODEL = "command-a-plus-05-2026"
HISTORY_TURN_CAP = 10
DEFAULT_NUM_QUESTIONS = 5

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
        "You are a quiz generator. Using ONLY the provided context, generate "
        "quiz questions that test understanding of the material relevant to "
        "the user's request. Respond ONLY with valid JSON — no preamble, no "
        "markdown fences — matching this schema exactly:\n"
        '{"questions": [{"question": str, "options": [str, str, str, str], '
        '"correct_answer": str, "citation": str}]}\n'
        "Each 'correct_answer' must exactly match one of the 'options'. Each "
        "'citation' should reference the bracketed source tag from the "
        "context that the question is drawn from. If the context is "
        "insufficient to generate meaningful questions, return "
        '{"questions": []}.'
    )

    messages = [{"role": "system", "content": system_instructions}]

    for turn in capped_history:
        role = "assistant" if turn.get("role") == "assistant" else "user"
        messages.append({"role": role, "content": turn.get("content", "")})

    user_turn = (
        f"Context:\n{formatted_context}\n\n"
        f"Request: {query}\n\n"
        f"Generate up to {DEFAULT_NUM_QUESTIONS} questions."
    )
    messages.append({"role": "user", "content": user_turn})

    return messages


def _format_questions_only(quiz_data: dict) -> str:
    """Render quiz questions + options WITHOUT answers — this is what gets
    shown to the student first (phase 1 of the two-phase flow)."""
    questions = quiz_data.get("questions", [])
    if not questions:
        return "I couldn't generate quiz questions from the available context."

    lines = []
    for i, q in enumerate(questions, start=1):
        lines.append(f"Q{i}. {q.get('question', '')}")
        for j, option in enumerate(q.get("options", []), start=1):
            lines.append(f"   {chr(96 + j)}) {option}")
        lines.append("")  # no Answer/Source lines — kept out of student view

    return "\n".join(lines).strip()


def run_quiz(
    query: str,
    chat_history: list[dict[str, str]],
    retrieved_context: list[dict],
) -> tuple[str, list[dict] | None]:
    """Returns (student_facing_questions, answer_key).

    answer_key: parsed list of question dicts (with correct_answer + citation),
    meant to be persisted by the calling node — NOT shown to the student
    directly. None if generation failed at any step.
    """
    capped_history = _cap_history(chat_history)
    formatted_context = _format_context(retrieved_context)
    messages = _build_prompt(query, formatted_context, capped_history)

    try:
        response = client.chat(model=MODEL, messages=messages)
        raw_text = _extract_text(response)
    except Exception:
        logger.exception("Quiz agent LLM call failed")
        return "I ran into an error trying to generate quiz questions. Please try again.", None

    if not raw_text:
        logger.error("Quiz agent received empty text response from model")
        return "I wasn't able to generate quiz questions for that. Please try rephrasing.", None

    try:
        quiz_data = json.loads(raw_text)
    except json.JSONDecodeError:
        logger.exception("Quiz agent failed to parse JSON response: %s", raw_text)
        return "I generated a response but couldn't format it as a quiz. Please try again.", None

    questions_string = _format_questions_only(quiz_data)
    answer_key = quiz_data.get("questions", [])
    return questions_string, answer_key