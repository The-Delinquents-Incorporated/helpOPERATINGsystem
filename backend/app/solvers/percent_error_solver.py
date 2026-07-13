from typing import Any, Dict
from backend.app.solvers.solver_base import ChemistrySolver

class PercentErrorSolver(ChemistrySolver):
    def solve_deterministic(self, theoretical: float, experimental: float) -> Dict[str, Any]:
        if theoretical == 0:
            raise ValueError("Theoretical value cannot be zero for percent error calculations.")
        
        error = ((experimental - theoretical) / theoretical) * 100
        magnitude = abs(error)
        
        # Simple qualitative interpretation
        if magnitude <= 5.0:
            interpretation = "Excellent / Acceptable experimental accuracy."
        elif magnitude <= 10.0:
            interpretation = "Moderate discrepancy, check for systematic or random errors."
        else:
            interpretation = "High error, significant experimental discrepancy."

        return {
            "theoretical": theoretical,
            "experimental": experimental,
            "error_percentage": round(error, 4),
            "magnitude": round(magnitude, 4),
            "interpretation": interpretation
        }

    def get_problem_statement(self, theoretical: float, experimental: float) -> str:
        return (
            f"Calculate the percent error and interpret the accuracy of this experimental result:\n"
            f"Theoretical value: {theoretical}\n"
            f"Experimental value: {experimental}"
        )
