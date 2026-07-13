import re
from typing import Any, Dict
from backend.app.solvers.solver_base import ChemistrySolver
from backend.app.core.chemistry import calculate_molar_mass

class StoichiometrySolver(ChemistrySolver):
    def parse_equation_coefficients(self, equation: str) -> Dict[str, float]:
        """Parses a chemical equation and returns a dict mapping formulas to their coefficients."""
        # Remove all spaces
        eq = equation.replace(" ", "")
        # Replace ->, =>, = with + to treat all species similarly for stoichiometry ratio lookup
        eq = re.sub(r'->|=>|=', '+', eq)
        species = eq.split('+')
        
        coefficients = {}
        for s in species:
            if not s:
                continue
            # Match optional coefficient (integer or decimal) at the start followed by formula
            match = re.match(r'^([\d\.]+)?([A-Za-z0-9_\(\)]+)', s)
            if match:
                coeff_str, formula = match.groups()
                coeff = float(coeff_str) if coeff_str else 1.0
                # Normalize chemical formula key
                coefficients[formula] = coeff
        return coefficients

    def solve_deterministic(self, equation: str, given_substance: str, given_value: float, given_unit: str, target_substance: str, target_unit: str) -> Dict[str, Any]:
        try:
            coefficients = self.parse_equation_coefficients(equation)
            if given_substance not in coefficients:
                # Try finding case-insensitive or partial matches
                matched = [k for k in coefficients.keys() if k.lower() == given_substance.lower()]
                if matched:
                    given_substance = matched[0]
                else:
                    raise ValueError(f"Given substance '{given_substance}' not found in chemical equation.")
            
            if target_substance not in coefficients:
                matched = [k for k in coefficients.keys() if k.lower() == target_substance.lower()]
                if matched:
                    target_substance = matched[0]
                else:
                    raise ValueError(f"Target substance '{target_substance}' not found in chemical equation.")

            given_coeff = coefficients[given_substance]
            target_coeff = coefficients[target_substance]

            # Molar masses
            given_molar_mass = calculate_molar_mass(given_substance)["molar_mass"]
            target_molar_mass = calculate_molar_mass(target_substance)["molar_mass"]

            # Convert given to moles
            if given_unit == "grams":
                given_moles = given_value / given_molar_mass
            elif given_unit == "liters":
                given_moles = given_value / 22.4
            elif given_unit == "particles":
                given_moles = given_value / 6.02e23
            elif given_unit == "moles":
                given_moles = given_value
            else:
                raise ValueError(f"Unsupported given unit: {given_unit}")

            # Stoichiometric mole ratio
            target_moles = given_moles * (target_coeff / given_coeff)

            # Convert target moles to target unit
            if target_unit == "grams":
                target_value = target_moles * target_molar_mass
            elif target_unit == "liters":
                target_value = target_moles * 22.4
            elif target_unit == "particles":
                target_value = target_moles * 6.02e23
            elif target_unit == "moles":
                target_value = target_moles
            else:
                raise ValueError(f"Unsupported target unit: {target_unit}")

            return {
                "equation": equation,
                "given_substance": given_substance,
                "given_value": given_value,
                "given_unit": given_unit,
                "target_substance": target_substance,
                "target_unit": target_unit,
                "result_value": round(target_value, 4),
                "given_molar_mass": given_molar_mass,
                "target_molar_mass": target_molar_mass,
                "mole_ratio": f"{target_coeff} : {given_coeff}"
            }
        except Exception as e:
            raise ValueError(f"Stoichiometry calculation failed: {e}")

    def get_problem_statement(self, equation: str, given_substance: str, given_value: float, given_unit: str, target_substance: str, target_unit: str) -> str:
        return (
            f"Solve the following stoichiometry problem:\n"
            f"Equation: {equation}\n"
            f"Given: {given_value} {given_unit} of {given_substance}\n"
            f"Find: How many {target_unit} of {target_substance} are produced/reacted?"
        )
