import pytest
from backend.app.solvers import EmpiricalMolecularSolver

def test_empirical_formula_glucose():
    solver = EmpiricalMolecularSolver()
    # Glucose: C: 40%, H: 6.7%, O: 53.3%
    res = solver.solve_deterministic(
        composition={"C": 40.0, "H": 6.7, "O": 53.3},
        molar_mass=180.16
    )
    assert res["empirical_formula"] == "CH2O"
    assert res["molecular_formula"] == "C6H12O6"
    assert res["molecular_multiplier"] == 6

def test_empirical_formula_no_molar_mass():
    solver = EmpiricalMolecularSolver()
    res = solver.solve_deterministic(
        composition={"C": 40.0, "H": 6.7, "O": 53.3}
    )
    assert res["empirical_formula"] == "CH2O"
    assert res["molecular_formula"] == "CH2O"
    assert res["molecular_multiplier"] == 1
