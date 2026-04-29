import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class ReviewerAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        else:
            self.llm = None

    def run(self, state: dict):
        task_input = state.get("task_input", "")
        execution_result = state.get("execution_result", "")
        revision_count = state.get("revision_count", 0)

        print(f"[Reviewer] Reviewing execution result. Revision: {revision_count}")
        
        if not self.llm:
            print("[Reviewer] Mocking review (No OPENAI_API_KEY found)")
            return {
                "is_approved": True, 
                "review_feedback": "Looks good.",
                "revision_count": revision_count + 1
            }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a strict Reviewer Agent. Review the execution result against the original task. If it fully solves the task, respond with exactly 'APPROVED'. If not, provide specific feedback on what needs to be fixed. DO NOT say APPROVED if there are missing parts."),
            ("user", "Original Task: {task_input}\n\nExecution Result:\n{execution_result}\n\nIs this approved?")
        ])
        chain = prompt | self.llm
        response = chain.invoke({
            "task_input": task_input, 
            "execution_result": execution_result
        })
        
        content = response.content.strip()
        is_approved = "APPROVED" in content.upper()
        
        return {
            "is_approved": is_approved,
            "review_feedback": content if not is_approved else "",
            "revision_count": revision_count + 1
        }
