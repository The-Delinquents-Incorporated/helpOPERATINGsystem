from typing import Any, Dict, Optional
import math
from backend.app.solvers.solver_base import ChemistrySolver
from backend.app.core.periodic_table import get_element
from backend.app.core.chemistry import calculate_molar_mass

class EmpiricalMolecularSolver(ChemistrySolver):
    def solve_deterministic(self, composition: Dict[str, float], molar_mass: Optional[float] = None) -> Dict[str, Any]:
        try:
            # 1. Convert composition to moles
            element_moles = {}
            for symbol, val in composition.items():
                el = get_element(symbol)
                if not el:
                    raise ValueError(f"Unknown element: {symbol}")
                element_moles[el.symbol] = val / el.mass

            # 2. Find minimum moles
            min_moles = min(element_moles.values())

            # 3. Get ratios
            ratios = {sym: m / min_moles for sym, m in element_moles.items()}

            # 4. Find multiplier to make all ratios integers (within 0.15 tolerance)
            multiplier = 1
            for m in range(1, 10):
                valid = True
                for sym, r in ratios.items():
                    val = r * m
                    if abs(val - round(val)) > 0.15:
                        valid = False
                        break
                if valid:
                    multiplier = m
                    break

            # Get empirical subscripts
            empirical_counts = {}
            for sym, r in ratios.items():
                empirical_counts[sym] = int(round(r * multiplier))

            # Build empirical formula string (e.g. C1H2O1 -> CH2O, but let's standardise order: C, then H, then others alphabetically, or keep user input order)
            # Standard order: C, then H, then others alphabetically
            def formula_str(counts: Dict[str, int]) -> str:
                sorted_keys = sorted(counts.keys())
                if "C" in counts:
                    sorted_keys.remove("C")
                    sorted_keys.insert(0, "C")
                    if "H" in counts:
                        sorted_keys.remove("H")
                        sorted_keys.insert(1, "H")
                parts = []
                for k in sorted_keys:
                    c = counts[k]
                    parts.append(f"{k}{c if c > 1 else ''}")
                return "".join(parts)

            empirical_formula = formula_str(empirical_counts)
            emp_mass_info = calculate_molar_mass(empirical_formula)
            empirical_molar_mass = emp_mass_info["molar_mass"]

            molecular_formula = empirical_formula
            molecular_molar_mass = empirical_molar_mass
            mol_multiplier = 1

            if molar_mass:
                mol_multiplier = int(round(molar_mass / empirical_molar_mass))
                if mol_multiplier < 1:
                    mol_multiplier = 1
                molecular_counts = {sym: c * mol_multiplier for sym, c in empirical_counts.items()}
                molecular_formula = formula_str(molecular_counts)
                molecular_molar_mass = calculate_molar_mass(molecular_formula)["molar_mass"]

            return {
                "empirical_formula": empirical_formula,
                "empirical_molar_mass": empirical_molar_mass,
                "molecular_formula": molecular_formula,
                "molecular_molar_mass": molecular_molar_mass,
                "empirical_counts": empirical_counts,
                "molecular_multiplier": mol_multiplier
            }
        except Exception as e:
            raise ValueError(f"Empirical/Molecular formula calculation failed: {e}")

    def get_problem_statement(self, composition: Dict[str, float], molar_mass: Optional[float] = None) -> str:
        comp_str = ", ".join([f"{k}: {v}%" for k, v in composition.items()])
        mass_str = f" with a molar mass of {molar_mass} g/mol" if molar_mass else ""
        return (
            f"Find the empirical and molecular formula of a compound with the following composition: "
            f"{comp_str}{mass_str}."
        )
