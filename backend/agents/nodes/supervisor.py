from routing.services.router import route_query
from agents.state import StudyCompanionState


def supervisor_node(state: StudyCompanionState) -> dict:
    """
    LangGraph node. Reads the query from state, runs it through the router,
    and returns the fields to update in state. LangGraph merges this dict
    back into the full state automatically — we don't return the whole state,
    just what changed.
    """
    agent, method = route_query(state["query"])

    return {
        "routing_decision": agent,
        "routing_method": method,
    }


def route_to_agent(state: StudyCompanionState) -> str:
    """
    Conditional edge function. NOT a graph node — LangGraph calls this
    separately, after supervisor_node runs, to decide which node name to
    jump to next. It just reads what supervisor_node already decided.
    """
    return state["routing_decision"]