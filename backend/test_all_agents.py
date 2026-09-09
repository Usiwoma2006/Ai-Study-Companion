import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # adjust to your actual settings module path
django.setup()

# Paste this into: python manage.py shell
# Adjust NOTEBOOK_ID to a real Notebook you already have ingested content for.

from agents.graph import app

NOTEBOOK_ID = 1  # <-- change to a real notebook id in your DB

test_cases = [
    {"label": "Tutor",             "query": "Explain how mitosis works"},
    {"label": "Quiz",              "query": "Quiz me on cell division"},
    {"label": "Study planner",     "query": "Help me plan what to study this week"},
    {"label": "Progress analysis", "query": "How am I doing so far with this material?"},
    {"label": "Research",          "query": "Compare mitosis and meiosis across my notes"},
]

results = []

for case in test_cases:
    print(f"\n{'=' * 60}")
    print(f"TEST: {case['label']}  —  query: {case['query']!r}")
    print("=" * 60)

    initial_state = {
        "query": case["query"],
        "notebook_id": NOTEBOOK_ID,
        "chat_history": [],
        "retrieved_context": [],
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
    print(f"  [{status}] {r['label']:20s} -> routed to: {r['routed_to']}")