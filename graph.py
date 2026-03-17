from langgraph.graph import StateGraph, END
from state import ResearchState
from planner_agent import run_planner
from executor import run_executor
from answer_agent import run_answering
from guardrail import run_guardrails # Import your new node

# 1. Initialize the graph
workflow = StateGraph(ResearchState)

# 2. Add nodes
workflow.add_node("guard", run_guardrails)
workflow.add_node("planner", run_planner)
workflow.add_node("executor", run_executor)
workflow.add_node("answer", run_answering)

# 3. Define the routing logic function
def check_safety(state: dict):
    if state.get("is_safe") == False:
        return "unsafe"
    return "safe"

# 4. Wire the execution flow
workflow.set_entry_point("guard")

# If safe, go to planner. If unsafe, skip straight to the END.
workflow.add_conditional_edges(
    "guard",
    check_safety,
    {
        "safe": "planner",
        "unsafe": END 
    }
)

workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "answer")
workflow.add_edge("answer", END)

app = workflow.compile()