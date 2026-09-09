"""
Agent nodes for the LangGraph study companion graph.

All five agents are now wired to their real services under agents/services/.
File retains the 'stubs' name for now since it's the established module path
referenced by graph.py — rename in a later pass if desired.
"""

import logging

from agents.services.progress_analysis_service import run_progress_analysis
from agents.services.quiz_service import run_quiz
from agents.services.research_service import run_research
from agents.services.study_planner_service import run_study_planner
from agents.services.tutor_service import run_tutor
from agents.state import StudyCompanionState
from notebooks.models import Quiz, QuizQuestion  # adjust if you placed these elsewhere

logger = logging.getLogger(__name__)


def tutor_agent(state: StudyCompanionState) -> StudyCompanionState:
    """Generates explanations grounded in retrieved_context, folding in
    capped chat history, query rewriting, and citation-aware context."""
    logger.info("Tutor agent invoked for query: %s", state["query"])

    state["agent_output"] = run_tutor(
        query=state["query"],
        chat_history=state.get("chat_history", []),
        retrieved_context=state.get("retrieved_context", []),
    )
    return state


def quiz_agent(state: StudyCompanionState) -> StudyCompanionState:
    """Generates quiz questions grounded in retrieved_context.

    Two-phase output (exception to the plain-string-only rule): agent_output
    holds only the questions/options shown to the student. Correct answers +
    citations are persisted to the database (Quiz/QuizQuestion), not stored
    in state, so they survive past this single invoke() call and can be read
    back by a later "check my answer" step."""
    logger.info("Quiz agent invoked for query: %s", state["query"])

    questions_string, answer_key = run_quiz(
        query=state["query"],
        chat_history=state.get("chat_history", []),
        retrieved_context=state.get("retrieved_context", []),
    )

    # Generation failed (answer_key is None) — nothing to persist, just
    # pass the error/fallback string straight through.
    if not answer_key:
        state["agent_output"] = questions_string
        return state

    # 1. Create the Quiz row, tied to this notebook.
    quiz = Quiz.objects.create(
        notebook_id=state["notebook_id"],
        query=state["query"],
    )

    # 2. Create one QuizQuestion row per question — correct_answer and
    #    citation live here, server-side only, never in agent_output.
    for i, q in enumerate(answer_key, start=1):
        QuizQuestion.objects.create(
            quiz=quiz,
            order=i,
            question_text=q.get("question", ""),
            options=q.get("options", []),
            correct_answer=q.get("correct_answer", ""),
            citation=q.get("citation", ""),
        )

    # 3. agent_output = student-facing questions + the quiz id, so a later
    #    turn knows which quiz to look up when the student answers.
    state["agent_output"] = f"{questions_string}\n\nQuiz ID: {quiz.id}"
    return state


def study_planner_agent(state: StudyCompanionState) -> StudyCompanionState:
    """Prioritizes study topics/actions based on retrieved_context and history."""
    logger.info("Study planner agent invoked for query: %s", state["query"])

    state["agent_output"] = run_study_planner(
        query=state["query"],
        chat_history=state.get("chat_history", []),
        retrieved_context=state.get("retrieved_context", []),
    )
    return state


def progress_analysis_agent(state: StudyCompanionState) -> StudyCompanionState:
    """Analyzes chat_history for learning patterns/struggle areas."""
    logger.info("Progress analysis agent invoked for query: %s", state["query"])

    state["agent_output"] = run_progress_analysis(
        query=state["query"],
        chat_history=state.get("chat_history", []),
        retrieved_context=state.get("retrieved_context", []),
    )
    return state


def research_agent(state: StudyCompanionState) -> StudyCompanionState:
    """Synthesizes an answer across multiple retrieved_context sources."""
    logger.info("Research agent invoked for query: %s", state["query"])

    state["agent_output"] = run_research(
        query=state["query"],
        chat_history=state.get("chat_history", []),
        retrieved_context=state.get("retrieved_context", []),
    )
    return state