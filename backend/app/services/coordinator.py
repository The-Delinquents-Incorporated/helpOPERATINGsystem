import json
import re
from typing import AsyncGenerator, Dict, List, Any, Optional
from backend.app.services.ollama import ollama_service
from backend.app.services.prompt_templates import SYSTEM_PROMPT
from backend.app.core.chemistry import (
    calculate_molar_mass,
    convert_grams_moles,
    convert_stp,
    calculate_avogadro
)
from backend.app.core.math import solve_math_expression

def parse_json_command(text: str) -> Optional[Dict[str, Any]]:
    """
    Robustly extract and parse a JSON tool command from LLM response text.
    Handles raw JSON as well as Markdown code blocks (```json ... ```).
    """
    clean_text = text.strip()
    
    # Try extracting from markdown fenced blocks first
    markdown_json_regex = r"```(?:json)?\s*(\{.*?\})\s*```"
    match = re.search(markdown_json_regex, clean_text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Check if the text contains a JSON structure
        json_structure_regex = r"(\{.*\})"
        match_structure = re.search(json_structure_regex, clean_text, re.DOTALL)
        if match_structure:
            json_str = match_structure.group(1)
        else:
            json_str = clean_text

    try:
        data = json.loads(json_str)
        if isinstance(data, dict) and "tool" in data:
            return data
    except json.JSONDecodeError:
        pass
        
    return None

def execute_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute deterministic Python function associated with the specified tool.
    """
    t_name = tool_name.strip().lower()
    
    if t_name == "molar_mass":
        formula = args.get("formula", "")
        return calculate_molar_mass(formula)
        
    elif t_name == "convert_grams_moles":
        formula = args.get("formula", "")
        value = float(args.get("value", 0))
        direction = args.get("direction", "")
        return convert_grams_moles(formula, value, direction)
        
    elif t_name == "stp_conversion":
        value = float(args.get("value", 0))
        direction = args.get("direction", "")
        return convert_stp(value, direction)
        
    elif t_name == "avogadro_calculation":
        value = float(args.get("value", 0))
        direction = args.get("direction", "")
        return calculate_avogadro(value, direction)
        
    elif t_name == "math_solve":
        expression = args.get("expression", "")
        return solve_math_expression(expression)
        
    else:
        raise ValueError(f"Unknown tool: '{tool_name}'")

class CoordinatorService:
    def _prepare_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Prepend system prompt to the user messages list.
        """
        prepared = [m.copy() for m in messages]
        # Check if system message already exists at the start
        if not prepared or prepared[0].get("role") != "system":
            prepared.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        else:
            # Append our instruction to existing system prompt
            prepared[0]["content"] = f"{prepared[0]['content']}\n\n{SYSTEM_PROMPT}"
        return prepared

    async def route_query(
        self, 
        messages: List[Dict[str, str]], 
        model: str = None
    ) -> Dict[str, Any]:
        """
        Non-streaming query coordinator. Routes requests to Mode A or Mode B.
        """
        prepared_messages = self._prepare_messages(messages)
        
        response = await ollama_service.generate_chat_completion(
            messages=prepared_messages,
            model=model,
            stream=False
        )
        
        content = response.get("message", {}).get("content", "")
        command = parse_json_command(content)
        
        if command:
            tool_name = command.get("tool")
            args = command.get("args", {})
            try:
                result = execute_tool(tool_name, args)
                return {
                    "mode": "deterministic",
                    "tool": tool_name,
                    "args": args,
                    "result": result
                }
            except Exception as e:
                return {
                    "mode": "error",
                    "detail": f"Failed to execute deterministic calculation: {str(e)}"
                }
        else:
            return {
                "mode": "reasoning",
                "content": content
            }

    async def route_query_stream(
        self, 
        messages: List[Dict[str, str]], 
        model: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Streaming query coordinator. Buffers potential JSON, yields tokens immediately for reasoning.
        """
        prepared_messages = self._prepare_messages(messages)
        
        generator = await ollama_service.generate_chat_completion(
            messages=prepared_messages,
            model=model,
            stream=True
        )
        
        buffer = ""
        is_json_candidate = None
        
        async for line in generator:
            try:
                chunk_data = json.loads(line)
            except json.JSONDecodeError:
                continue
                
            content = chunk_data.get("message", {}).get("content", "")
            buffer += content
            
            if is_json_candidate is None:
                stripped = buffer.strip()
                if len(stripped) > 0:
                    # Check if starting character implies a JSON command block
                    if stripped.startswith("{") or stripped.startswith("`"):
                        is_json_candidate = True
                    else:
                        is_json_candidate = False
                        # Flush the buffer as conversational reasoning content
                        yield json.dumps({"mode": "reasoning", "content": buffer, "done": False})
                        buffer = ""
                        
            elif is_json_candidate is False:
                # Real-time conversational streaming
                yield json.dumps({"mode": "reasoning", "content": content, "done": False})
                
        # Final processing
        if is_json_candidate is True:
            command = parse_json_command(buffer)
            if command:
                tool_name = command.get("tool")
                args = command.get("args", {})
                try:
                    result = execute_tool(tool_name, args)
                    yield json.dumps({
                        "mode": "deterministic",
                        "tool": tool_name,
                        "args": args,
                        "result": result,
                        "done": True
                    })
                except Exception as e:
                    yield json.dumps({
                        "mode": "error",
                        "detail": f"Failed to execute tool '{tool_name}': {str(e)}",
                        "done": True
                    })
            else:
                # Fallback to conversational mode if it failed to parse
                yield json.dumps({"mode": "reasoning", "content": buffer, "done": True})
        else:
            yield json.dumps({"mode": "reasoning", "content": "", "done": True})

coordinator_service = CoordinatorService()
