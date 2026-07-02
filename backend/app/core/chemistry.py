from typing import Dict, Any

def calculate_molar_mass(formula: str) -> Dict[str, Any]:
    """
    Stub for molar mass calculation.
    """
    formula_clean = formula.strip()
    # Simple hardcoded mock values for standard testing
    mock_masses = {
        "H2O": 18.02,
        "CO2": 44.01,
        "O2": 32.00,
        "NaCl": 58.44
    }
    
    mass = mock_masses.get(formula_clean, 100.0)  # Default fallback mass
    return {
        "formula": formula_clean,
        "molar_mass": mass,
        "unit": "g/mol",
        "is_mock": True
    }

def convert_grams_moles(formula: str, value: float, direction: str) -> Dict[str, Any]:
    """
    Stub for grams <-> moles conversions.
    direction must be "grams_to_moles" or "moles_to_grams".
    """
    molar_mass_info = calculate_molar_mass(formula)
    molar_mass = molar_mass_info["molar_mass"]
    
    if direction == "grams_to_moles":
        # moles = grams / molar_mass
        result = value / molar_mass
        output_unit = "moles"
    elif direction == "moles_to_grams":
        # grams = moles * molar_mass
        result = value * molar_mass
        output_unit = "grams"
    else:
        raise ValueError(f"Invalid direction: {direction}. Must be 'grams_to_moles' or 'moles_to_grams'")
        
    return {
        "formula": formula,
        "input_value": value,
        "direction": direction,
        "result": round(result, 4),
        "unit": output_unit,
        "is_mock": True
    }

def convert_stp(value: float, direction: str) -> Dict[str, Any]:
    """
    Stub for STP conversions (liters <-> moles).
    At STP, 1 mole of ideal gas occupies 22.4 liters.
    direction must be "liters_to_moles" or "moles_to_liters".
    """
    molar_volume = 22.4
    if direction == "liters_to_moles":
        result = value / molar_volume
        output_unit = "moles"
    elif direction == "moles_to_liters":
        result = value * molar_volume
        output_unit = "liters"
    else:
        raise ValueError(f"Invalid direction: {direction}. Must be 'liters_to_moles' or 'moles_to_liters'")
        
    return {
        "input_value": value,
        "direction": direction,
        "result": round(result, 4),
        "unit": output_unit,
        "is_mock": True
    }

def calculate_avogadro(value: float, direction: str) -> Dict[str, Any]:
    """
    Stub for Avogadro calculations (moles <-> particles).
    Avogadro's number is 6.02e23.
    direction must be "moles_to_particles" or "particles_to_moles".
    """
    avogadro = 6.02e23
    if direction == "moles_to_particles":
        result = value * avogadro
        output_unit = "particles"
    elif direction == "particles_to_moles":
        result = value / avogadro
        output_unit = "moles"
    else:
        raise ValueError(f"Invalid direction: {direction}. Must be 'moles_to_particles' or 'particles_to_moles'")
        
    return {
        "input_value": value,
        "direction": direction,
        "result": result,
        "unit": output_unit,
        "is_mock": True
    }
