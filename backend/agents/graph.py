"""
Supervisor routes to one of 5 agents based on heuristic/LLM classification;
each agent is currently a stub for testing the routing mechanics.
This graph implements a supervisor-worker pattern where the supervisor node
determines which specialized agent should handle each user request.
"""

from langgraph.graph import START, END, StateGraph
from agents.state import StudyCompanionState
from agents.nodes.supervisor import supervisor_node, route_to_agent
from agents.nodes.stubs import tutor_agent, quiz_agent, study_planner_agent, progress_analysis_agent, research_agent

graph = StateGraph(StudyCompanionState)

# Entry point - supervisor decides which agent to route to
graph.add_node("supervisor", supervisor_node)

# Worker agents (each handles a specific learning domain)
graph.add_node("tutor", tutor_agent)
graph.add_node("quiz", quiz_agent)
graph.add_node("study_planner", study_planner_agent)
graph.add_node("progress_analysis", progress_analysis_agent)
graph.add_node("research", research_agent)

# Define the flow: start → supervisor → conditional routing → agent → end
graph.add_edge(START, "supervisor")

graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "tutor": "tutor",
        "quiz": "quiz",
        "study_planner": "study_planner",
        "progress_analysis": "progress_analysis",
        "research": "research",
    },
)

# Each agent terminates the workflow
graph.add_edge("tutor", END)
graph.add_edge("quiz", END)
graph.add_edge("study_planner", END)
graph.add_edge("progress_analysis", END)
graph.add_edge("research", END)

app = graph.compile()