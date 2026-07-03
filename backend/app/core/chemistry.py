import re
from collections import defaultdict
from typing import Any, Dict

from backend.app.core.periodic_table import get_element

_SUBSCRIPT_TRANSLATION = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
_UNDERSCORE_SUBSCRIPT = re.compile(r"_(\d+)")


def normalize_formula(formula: str) -> str:
    """Normalize display-friendly formula text into parser-friendly notation."""
    clean = (formula or "").strip().replace(" ", "")
    clean = _UNDERSCORE_SUBSCRIPT.sub(r"\1", clean)
    return clean.translate(_SUBSCRIPT_TRANSLATION)


def parse_formula(formula: str) -> Dict[str, int]:
    """Parse a chemical formula with nested parentheses into element counts."""
    clean = normalize_formula(formula)
    if not clean:
        raise ValueError("Chemical formula is required")

    index = 0

    def parse_group(in_parentheses: bool = False) -> Dict[str, int]:
        nonlocal index
        counts: Dict[str, int] = defaultdict(int)
        while index < len(clean):
            char = clean[index]
            if char == "(":
                index += 1
                group_counts = parse_group(True)
                multiplier = parse_number()
                for symbol, count in group_counts.items():
                    counts[symbol] += count * multiplier
            elif char == ")":
                if not in_parentheses:
                    raise ValueError(f"Unmatched closing parenthesis in {formula}")
                index += 1
                return counts
            elif char.isupper():
                symbol = char
                index += 1
                if index < len(clean) and clean[index].islower():
                    symbol += clean[index]
                    index += 1
                if get_element(symbol) is None:
                    raise ValueError(f"Unknown element symbol: {symbol}")
                counts[symbol] += parse_number()
            else:
                raise ValueError(f"Invalid formula syntax near '{char}' in {formula}")
        if in_parentheses:
            raise ValueError(f"Unmatched opening parenthesis in {formula}")
        return counts

    def parse_number() -> int:
        nonlocal index
        start = index
        while index < len(clean) and clean[index].isdigit():
            index += 1
        return int(clean[start:index] or "1")

    parsed = parse_group()
    if index != len(clean):
        raise ValueError(f"Invalid formula syntax in {formula}")
    return dict(parsed)


def calculate_molar_mass(formula: str) -> Dict[str, Any]:
    """Calculate molar mass from the shared CDE/CAST periodic table."""
    formula_clean = normalize_formula(formula)
    composition = parse_formula(formula_clean)
    contributions = {}
    total = 0.0
    for symbol, count in composition.items():
        element = get_element(symbol)
        if element is None:
            raise ValueError(f"Unknown element symbol: {symbol}")
        subtotal = element.mass * count
        total += subtotal
        contributions[symbol] = {
            "count": count,
            "atomic_mass": element.mass,
            "subtotal": round(subtotal, 4),
        }

    return {
        "formula": formula_clean,
        "composition": composition,
        "contributions": contributions,
        "molar_mass": round(total, 2),
        "unit": "g/mol",
        "is_mock": False,
    }


def convert_grams_moles(formula: str, value: float, direction: str) -> Dict[str, Any]:
    """Convert grams <-> moles using the shared molar-mass engine."""
    molar_mass_info = calculate_molar_mass(formula)
    molar_mass = molar_mass_info["molar_mass"]

    if direction == "grams_to_moles":
        result = value / molar_mass
        output_unit = "moles"
    elif direction == "moles_to_grams":
        result = value * molar_mass
        output_unit = "grams"
    else:
        raise ValueError(f"Invalid direction: {direction}. Must be 'grams_to_moles' or 'moles_to_grams'")

    return {
        "formula": molar_mass_info["formula"],
        "molar_mass": molar_mass,
        "input_value": value,
        "direction": direction,
        "result": round(result, 4),
        "unit": output_unit,
        "is_mock": False,
    }


def convert_stp(value: float, direction: str) -> Dict[str, Any]:
    """Convert liters <-> moles at STP using 22.4 L/mol."""
    molar_volume = 22.4
    if direction == "liters_to_moles":
        result = value / molar_volume
        output_unit = "moles"
    elif direction == "moles_to_liters":
        result = value * molar_volume
        output_unit = "liters"
    else:
        raise ValueError(f"Invalid direction: {direction}. Must be 'liters_to_moles' or 'moles_to_liters'")

    return {"input_value": value, "direction": direction, "result": round(result, 4), "unit": output_unit, "is_mock": False}


def calculate_avogadro(value: float, direction: str) -> Dict[str, Any]:
    """Convert moles <-> particles using Avogadro's number."""
    avogadro = 6.02e23
    if direction == "moles_to_particles":
        result = value * avogadro
        output_unit = "particles"
    elif direction == "particles_to_moles":
        result = value / avogadro
        output_unit = "moles"
    else:
        raise ValueError(f"Invalid direction: {direction}. Must be 'moles_to_particles' or 'particles_to_moles'")

    return {"input_value": value, "direction": direction, "result": result, "unit": output_unit, "is_mock": False}
