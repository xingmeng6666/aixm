from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.reviewer import ReviewerAgent

class GraphState(TypedDict):
    task_input: str
    plan: str
    execution_result: str
    review_feedback: str
    revision_count: int
    is_approved: bool

class Orchestrator:
    """
    Coordinates different agents using LangGraph for a stateful, cyclic workflow.
    Workflow: Planner -> Executor -> Reviewer -> (if failed, back to Executor) -> END
    """
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.reviewer = ReviewerAgent()
        self.workflow = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(GraphState)

        # Define nodes
        workflow.add_node("planner", self.planner.run)
        workflow.add_node("executor", self.executor.run)
        workflow.add_node("reviewer", self.reviewer.run)

        # Define basic edges
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", "reviewer")

        # Define conditional edges
        def reviewer_router(state: GraphState):
            if state.get("is_approved") or state.get("revision_count", 0) >= 3:
                return "end"
            return "executor" # Loop back to executor with feedback

        workflow.add_conditional_edges(
            "reviewer",
            reviewer_router,
            {
                "end": END,
                "executor": "executor"
            }
        )
        return workflow.compile()

    def route_task(self, task_type: str, payload: dict):
        """
        Routes the task using the LangGraph workflow.
        """
        task_input = payload.get("input", str(payload))
        initial_state = {
            "task_input": task_input,
            "plan": "",
            "execution_result": "",
            "review_feedback": "",
            "revision_count": 0,
            "is_approved": False
        }
        
        print(f"[Orchestrator] Starting LangGraph flow for task: {task_input}")
        result = self.workflow.invoke(initial_state)
        return result

orchestrator = Orchestrator()
