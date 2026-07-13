from typing import Any, Dict
from backend.app.solvers.solver_base import ChemistrySolver
from backend.app.core.chemistry import calculate_molar_mass

class PercentCompositionSolver(ChemistrySolver):
    def solve_deterministic(self, formula: str) -> Dict[str, Any]:
        try:
            molar_mass_info = calculate_molar_mass(formula)
            total_mass = molar_mass_info["molar_mass"]
            
            percentages = {}
            for symbol, details in molar_mass_info["contributions"].items():
                subtotal = details["subtotal"]
                pct = (subtotal / total_mass) * 100
                percentages[symbol] = round(pct, 2)

            return {
                "formula": molar_mass_info["formula"],
                "molar_mass": total_mass,
                "percentages": percentages,
                "contributions": molar_mass_info["contributions"]
            }
        except Exception as e:
            raise ValueError(f"Percent composition calculation failed: {e}")

    def get_problem_statement(self, formula: str) -> str:
        return f"Calculate the percent composition by mass for each element in the chemical formula: {formula}."
