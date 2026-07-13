import pytest
from backend.app.solvers import StoichiometrySolver

def test_stoichiometry_moles_to_moles():
    solver = StoichiometrySolver()
    # 2H2 + O2 -> 2H2O. 2 moles of H2 should give 2 moles of H2O.
    res = solver.solve_deterministic(
        equation="2H2 + O2 -> 2H2O",
        given_substance="H2",
        given_value=2.0,
        given_unit="moles",
        target_substance="H2O",
        target_unit="moles"
    )
    assert res["result_value"] == 2.0

def test_stoichiometry_grams_to_grams():
    solver = StoichiometrySolver()
    # 2H2 + O2 -> 2H2O.
    # H2 mass = 2.02 g/mol, H2O mass = 18.02 g/mol.
    # 4.04 g of H2 (2 moles) -> 2 moles of H2O -> 36.04 g of H2O.
    res = solver.solve_deterministic(
        equation="2H2 + O2 -> 2H2O",
        given_substance="H2",
        given_value=4.04,
        given_unit="grams",
        target_substance="H2O",
        target_unit="grams"
    )
    # The solver uses hydrogen (1.01) * 2 = 2.02. water (1.01 * 2 + 16.0) = 18.02.
    assert round(res["result_value"], 2) == 36.04

def test_stoichiometry_invalid_substance():
    solver = StoichiometrySolver()
    with pytest.raises(ValueError):
        solver.solve_deterministic(
            equation="2H2 + O2 -> 2H2O",
            given_substance="CO2",
            given_value=2.0,
            given_unit="moles",
            target_substance="H2O",
            target_unit="moles"
        )
