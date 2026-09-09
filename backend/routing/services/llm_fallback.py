import os
import json
import cohere

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
client = cohere.ClientV2(api_key=COHERE_API_KEY)

VALID_AGENTS = {"tutor", "quiz", "study_planner", "progress_analysis", "research"}

SYSTEM_PROMPT = """You are a routing classifier for a study companion app. Given a user's query, decide which single agent should handle it.

Agents:
- tutor: explains concepts, answers "what is X" / "why does X work" questions, general subject help
- quiz: generates practice questions, tests the student, homework/assignment help
- study_planner: builds schedules, plans study sessions, time management
- progress_analysis: reviews performance, identifies weak/strong areas, tracks improvement over time
- research: finds external/outside sources beyond the student's own notes

Respond with ONLY a JSON object, no preamble, no markdown fences, in this exact shape:
{"agent": "<one of: tutor, quiz, study_planner, progress_analysis, research>"}
"""

def llm_route(query: str) -> str:
    """
    Last-resort classifier for queries the heuristic layer couldn't confidently route.
    Always returns a valid agent label — defaults to 'tutor' if parsing fails
    or the model returns something outside the known agent set.
    """
    response = client.chat(
        model="command-a-plus-05-2026",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        temperature=0,
    )

    # Same gotcha as context_compressor.py: filter for type == "text",
    # this model can also return a type == "thinking" block.
    text_blocks = [
        block.text for block in response.message.content
        if getattr(block, "type", None) == "text"
    ]
    raw_text = "".join(text_blocks).strip()

    try:
        parsed = json.loads(raw_text)
        agent = parsed.get("agent", "").strip().lower()
        if agent in VALID_AGENTS:
            return agent
    except json.JSONDecodeError:
        pass

    # Fallback of last resort: tutor is the safest generic default
    return "tutor"