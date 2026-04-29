import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from tools.langchain_tools import search_web, send_email, post_tweet

class ExecutorAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.tools = [search_web, send_email, post_tweet]
        
        if self.api_key:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a diligent Executor Agent. Execute the provided plan step-by-step using the available tools. Do your best to complete all steps."),
                ("user", "Task Input: {task_input}\n\nPlan to execute:\n{plan}\n\nReviewer Feedback (if any): {review_feedback}\n\nPlease execute the plan and provide the final result."),
                ("placeholder", "{agent_scratchpad}"),
            ])
            self.agent = create_tool_calling_agent(self.llm, self.tools, prompt)
            self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
        else:
            self.agent_executor = None

    def run(self, state: dict):
        plan = state.get("plan", "")
        task_input = state.get("task_input", "")
        review_feedback = state.get("review_feedback", "")
        
        print(f"[Executor] Executing plan: {plan[:50]}...")
        
        if not self.agent_executor:
            print("[Executor] Mocking execution (No OPENAI_API_KEY found)")
            mock_result = f"Mock execution successful based on plan: {plan}"
            return {"execution_result": mock_result}
        
        result = self.agent_executor.invoke({
            "task_input": task_input,
            "plan": plan,
            "review_feedback": review_feedback
        })
        
        return {"execution_result": result["output"]}
