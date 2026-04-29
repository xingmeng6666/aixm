import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class PlannerAgent:
    def __init__(self):
        # Allow fallback for missing API key for demonstration purposes
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        else:
            self.llm = None

    def run(self, state: dict):
        task_input = state.get("task_input", "")
        print(f"[Planner] Planning task: {task_input}")
        
        if not self.llm:
            print("[Planner] Mocking response (No OPENAI_API_KEY found)")
            mock_plan = f"1. Analyze '{task_input}'\n2. Use crawler if needed\n3. Format result\n4. Dispatch email/tweet"
            return {"plan": mock_plan}
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert AI Planner. Break down the user's request into a clear, actionable step-by-step plan. Only output the steps."),
            ("user", "Task: {task_input}")
        ])
        chain = prompt | self.llm
        response = chain.invoke({"task_input": task_input})
        
        return {"plan": response.content}
