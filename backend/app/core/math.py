from typing import Dict, Any
import re

def solve_math_expression(expression: str) -> Dict[str, Any]:
    """
    Stub/Basic solver for mathematical expressions.
    Safely evaluates simple mathematical expressions or returns mock results.
    """
    clean_expr = expression.strip()
    eval_expr = clean_expr.replace('^', '**')
    
    # Safe evaluation of basic math symbols only (numbers, +, -, *, /, exponents, ., parenthesises)
    if re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', eval_expr):
        try:
            # Note: eval is safe here because we regex-restricted the input to math characters
            result = eval(eval_expr, {"__builtins__": None}, {})
            return {
                "expression": clean_expr,
                "result": result,
                "success": True,
                "is_mock": False
            }
        except Exception as e:
            return {
                "expression": clean_expr,
                "error": f"Evaluation error: {str(e)}",
                "success": False,
                "is_mock": True
            }
    
    # Default mock result for complex equations (like x^2 + 5x + 6 = 0)
    return {
        "expression": clean_expr,
        "result": "x = -2, x = -3 (mock answer)",
        "success": True,
        "is_mock": True
    }
