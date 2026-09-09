import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from agents.graph import app
from notebooks.models import Quiz, QuizQuestion  # adjust import if placed elsewhere
from retrieval.services.retrieve_rerank_compress import retrieve_rerank_compress  # adjust path if different

NOTEBOOK_ID = 2  # <-- change to a real notebook id with ingested content

test_cases = [
    {"label": "Quiz",                        "query": "Quiz me on compound interest"},
    {"label": "Research (should hit notes)", "query": "Compare simple interest and compound interest based on my notes"},
    
]

results = []

for case in test_cases:
    print(f"\n{'=' * 60}")
    print(f"TEST: {case['label']}  —  query: {case['query']!r}")
    print("=" * 60)

    # Pull real retrieved_context, same as the production pipeline would.
    try:
        retrieved_context = retrieve_rerank_compress(case["query"], NOTEBOOK_ID)
        print(f"(retrieved {len(retrieved_context)} context chunks)")
    except Exception as e:
        print(f"Retrieval failed, falling back to empty context: {e!r}")
        retrieved_context = []

    initial_state = {
        "query": case["query"],
        "notebook_id": NOTEBOOK_ID,
        "chat_history": [],
        "retrieved_context": retrieved_context,
        "routing_decision": "",
        "routing_method": "heuristic",
        "agent_output": None,
    }

    try:
        final_state = app.invoke(initial_state)
        routed_to = final_state.get("routing_decision")
        method = final_state.get("routing_method")
        output = final_state.get("agent_output")

        print(f"Routed to: {routed_to}  (method: {method})")
        print("-" * 60)
        print(output)

        results.append({"label": case["label"], "routed_to": routed_to, "ok": bool(output)})
    except Exception as e:
        print(f"ERROR: {e!r}")
        results.append({"label": case["label"], "routed_to": None, "ok": False})

print(f"\n{'=' * 60}")
print("SUMMARY")
print("=" * 60)
for r in results:
    status = "OK" if r["ok"] else "FAILED"
    print(f"  [{status}] {r['label']:35s} -> routed to: {r['routed_to']}")

# Quiz DB check — confirm rows were actually created with answers stored
print(f"\n{'=' * 60}")
print("QUIZ DB CHECK")
print("=" * 60)
latest_quiz = Quiz.objects.filter(notebook_id=NOTEBOOK_ID).order_by("-created_at").first()
if latest_quiz:
    print(f"Latest Quiz: {latest_quiz.id}  (query: {latest_quiz.query!r})")
    for q in latest_quiz.questions.all():
        print(f"  Q{q.order}: {q.question_text}")
        print(f"     options: {q.options}")
        print(f"     correct_answer: {q.correct_answer}")
        print(f"     citation: {q.citation}")
else:
    print("No Quiz row found — quiz_agent may not have persisted correctly.")