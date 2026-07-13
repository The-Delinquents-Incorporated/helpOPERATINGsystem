import os
import re
from abc import ABC, abstractmethod
from typing import Any, Dict
from backend.app.services.ollama import ollama_service

class ChemistrySolver(ABC):
    def __init__(self):
        self.prompt_template_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prompts",
            "chemistry_work_explanation.txt"
        )

    def load_prompt_template(self) -> str:
        with open(self.prompt_template_path, "r", encoding="utf-8") as f:
            return f.read()

    async def call_ollama(self, problem_statement: str, show_work: bool) -> str:
        template = self.load_prompt_template()
        show_work_instruction = (
            "Explain step-by-step how to solve the problem, showing the math. Be clear and educational."
            if show_work else
            "Do NOT explain anything. Provide ONLY the final answer as a raw value or formula."
        )
        
        prompt = template.format(
            show_work_instruction=show_work_instruction,
            problem_statement=problem_statement
        )
        
        messages = [{"role": "user", "content": prompt}]
        try:
            response = await ollama_service.generate_chat_completion(
                messages=messages,
                stream=False
            )
            return response.get("message", {}).get("content", "").strip()
        except Exception as e:
            return f"Error generating explanation: {e}"

    @abstractmethod
    def solve_deterministic(self, **kwargs) -> Dict[str, Any]:
        """Compute the result deterministically using Python logic."""
        pass

    @abstractmethod
    def get_problem_statement(self, **kwargs) -> str:
        """Construct the prompt/problem statement for Ollama."""
        pass

    async def solve(self, show_work: bool = False, **kwargs) -> Dict[str, Any]:
        # 1. Calculate the exact deterministic result
        deterministic_result = self.solve_deterministic(**kwargs)
        
        # 2. If show_work is enabled, get explanation from Ollama
        explanation = ""
        if show_work:
            problem = self.get_problem_statement(**kwargs)
            explanation = await self.call_ollama(problem, show_work=True)
        else:
            explanation = "Work explanation disabled."

        return {
            "result": deterministic_result,
            "explanation": explanation,
            "show_work": show_work
        }
