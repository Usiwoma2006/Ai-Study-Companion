import os
import django

# --------------------------------------------------
# 1. Bootstrap Django
# --------------------------------------------------

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


# --------------------------------------------------
# 2. Import the services we want to test
# --------------------------------------------------

from agents.services.study_planner_service import run_study_planner
from agents.services.progress_analysis_service import run_progress_analysis


# --------------------------------------------------
# 3. Realistic multi-turn conversation
# --------------------------------------------------

chat_history = [
    {
        "role": "user",
        "content": "Can you explain compound interest to me?"
    },
    {
        "role": "assistant",
        "content": (
            "Compound interest is interest calculated on both the original "
            "principal and the interest accumulated from previous periods."
        )
    },
    {
        "role": "user",
        "content": (
            "I understand that interest is added, but I don't understand "
            "why compound interest grows faster."
        )
    },
    {
        "role": "assistant",
        "content": (
            "It grows faster because each new period can earn interest on "
            "the interest that was added during earlier periods."
        )
    },
    {
        "role": "user",
        "content": (
            "Okay, but I am confused about the formula. What does each "
            "part of the compound interest formula mean?"
        )
    },
    {
        "role": "assistant",
        "content": (
            "In A = P(1 + r/n)^(nt), P is the principal, r is the annual "
            "interest rate, n is the number of times interest is compounded "
            "per year, t is the time, and A is the final amount."
        )
    },
    {
        "role": "user",
        "content": (
            "Can you give me another example? I still don't know how "
            "changing the interest rate affects the final amount."
        )
    },
    {
        "role": "assistant",
        "content": (
            "For example, increasing the interest rate while keeping the "
            "principal and time constant will generally increase the final "
            "amount because each compounding period produces more interest."
        )
    },
]


# --------------------------------------------------
# 4. Retrieved context
# --------------------------------------------------

retrieved_context = [
    {
        "document_title": "Mathematics Notes",
        "section_title": "Compound Interest",
        "page_number": 12,
        "content": (
            "Compound interest is calculated on the principal and also on "
            "interest accumulated during previous periods. The formula is "
            "A = P(1 + r/n)^(nt)."
        ),
    },
    {
        "document_title": "Mathematics Notes",
        "section_title": "Interest Rates",
        "page_number": 13,
        "content": (
            "When other variables remain constant, a higher interest rate "
            "generally produces a larger final amount."
        ),
    },
]


# --------------------------------------------------
# 5. Test Study Planner
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST 1: STUDY PLANNER")
print("=" * 60)

study_plan = run_study_planner(
    query="Based on my recent learning, what should I study next?",
    chat_history=chat_history,
    retrieved_context=retrieved_context,
)

print("\nSTUDY PLAN:\n")
print(study_plan)


# --------------------------------------------------
# 6. Test Progress Analysis
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST 2: PROGRESS ANALYSIS")
print("=" * 60)

progress_analysis = run_progress_analysis(
    query=(
        "Analyze my recent learning and identify recurring struggles, "
        "topics I have revisited, and areas where I may need more practice."
    ),
    chat_history=chat_history,
    retrieved_context=retrieved_context,
)

print("\nPROGRESS ANALYSIS:\n")
print(progress_analysis)


# --------------------------------------------------
# 7. Test insufficient history
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST 3: INSUFFICIENT HISTORY")
print("=" * 60)

short_history = [
    {
        "role": "user",
        "content": "What is photosynthesis?"
    }
]

short_analysis = run_progress_analysis(
    query="Analyze my learning progress and identify my recurring struggles.",
    chat_history=short_history,
    retrieved_context=[],
)

print("\nSHORT-HISTORY ANALYSIS:\n")
print(short_analysis)


# --------------------------------------------------
# 8. Test history cap
# --------------------------------------------------

print("\n" + "=" * 60)
print("TEST 4: HISTORY CAP")
print("=" * 60)

long_history = []

for i in range(15):
    long_history.append(
        {
            "role": "user",
            "content": f"Student question {i + 1}"
        }
    )
    long_history.append(
        {
            "role": "assistant",
            "content": f"Assistant response {i + 1}"
        }
    )

print(f"\nOriginal history length: {len(long_history)}")

from agents.services.study_planner_service import _cap_history

capped_history = _cap_history(long_history)

print(f"Capped history length: {len(capped_history)}")
print("\nLast retained turn:")
print(capped_history[-1])

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)