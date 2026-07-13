import pytest
from backend.app.solvers import PercentCompositionSolver

def test_percent_composition_water():
    solver = PercentCompositionSolver()
    res = solver.solve_deterministic(formula="H2O")
    # H2O molar mass = 18.02. H: 2.02 / 18.02 = 11.21%. O: 16.0 / 18.02 = 88.79%
    assert res["formula"] == "H2O"
    assert res["percentages"]["H"] == 11.21
    assert res["percentages"]["O"] == 88.79

def test_percent_composition_complex():
    solver = PercentCompositionSolver()
    res = solver.solve_deterministic(formula="Ca(OH)2")
    # Ca=40.08, O=16.0*2=32.0, H=1.01*2=2.02. Total = 74.1.
    # Ca: 40.08/74.1 = 54.09%
    # O: 32.0/74.1 = 43.18%
    # H: 2.02/74.1 = 2.73%
    assert res["percentages"]["Ca"] == 54.09
    assert res["percentages"]["O"] == 43.18
    assert res["percentages"]["H"] == 2.73
