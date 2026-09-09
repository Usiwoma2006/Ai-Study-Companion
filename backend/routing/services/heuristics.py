# Order matters: dict is scanned top-to-bottom, first match wins.
# Rule: most specific, high-precision phrases first (low risk of false-positive
# overlap with other agents), most generic/catch-all phrases last.
# Generic single/two-word triggers (e.g. "what is", "explain") are intentionally
# excluded — too ambiguous, left for the LLM fallback to resolve using full context.
ROUTING_KEYWORDS = {
    # --- high-precision, unlikely to overlap with other categories ---
    "study_planner": ["study plan", "schedule", "when should i study", "plan my week"],
    "progress_analysis": ["how am i doing", "my progress", "weak areas", "strong areas", "am i improving"],
    "research": ["find more on", "look up", "outside sources", "beyond my notes"],
    "quiz": ["quiz me", "test me", "practice questions", "give me questions", "assignment", "classwork", "homework"],

    # --- broader/catch-all, checked last so more specific agents get first pick ---
    "tutor": ["teach me", "tutor me", "explain to me", "can you explain"],
}

def heuristic_route(query: str) -> str | None:
    q = query.lower()
    for agent, patterns in ROUTING_KEYWORDS.items():
        if any(p in q for p in patterns):
            return agent
    return None  # signals "fall through to LLM"