from typing import TypedDict, Literal

class StudyCompanionState(TypedDict):
    query: str
    notebook_id: int
    chat_history: list[dict[str, str]]
    retrieved_context: list[dict]
    routing_decision: str
    routing_method: Literal["heuristic", "llm_fallback", "llm_fallback_error"]
    agent_output: str | None
    quiz_answer_key: list[dict] | None