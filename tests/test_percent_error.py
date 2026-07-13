import pytest
from backend.app.solvers import PercentErrorSolver

def test_percent_error_success():
    solver = PercentErrorSolver()
    res = solver.solve_deterministic(theoretical=18.02, experimental=17.8)
    # ((17.8 - 18.02) / 18.02) * 100 = -1.2209%
    assert round(res["error_percentage"], 2) == -1.22
    assert round(res["magnitude"], 2) == 1.22
    assert "Excellent" in res["interpretation"]

def test_percent_error_zero_theoretical():
    solver = PercentErrorSolver()
    with pytest.raises(ValueError):
        solver.solve_deterministic(theoretical=0.0, experimental=10.0)
