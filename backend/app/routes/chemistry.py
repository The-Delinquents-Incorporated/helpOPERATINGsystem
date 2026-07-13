from typing import Optional, Dict, List, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.coordinator import execute_tool
from backend.app.solvers import (
    StoichiometrySolver,
    EmpiricalMolecularSolver,
    PercentCompositionSolver,
    PercentErrorSolver
)
from backend.app.knowledge_base import KBSearch

router = APIRouter(prefix="/api/chemistry", tags=["Chemistry"])

# Instantiate solvers and search index
stoichiometry_solver = StoichiometrySolver()
empirical_molecular_solver = EmpiricalMolecularSolver()
percent_composition_solver = PercentCompositionSolver()
percent_error_solver = PercentErrorSolver()
kb_search_index = KBSearch()

class ChemistryCalculateRequest(BaseModel):
    tool: str = Field(..., description="Chemistry tool name (molar_mass, convert_grams_moles, etc.)")
    formula: Optional[str] = Field(None, description="Chemical formula")
    value: Optional[float] = Field(None, description="Numeric input for conversions")
    direction: Optional[str] = Field(None, description="Conversion direction for applicable tools")

@router.post("/calculate")
async def calculate(request: ChemistryCalculateRequest):
    """Run a chemistry calculation directly without routing through the AI coordinator."""
    args = {}
    if request.formula is not None:
        args["formula"] = request.formula
    if request.value is not None:
        args["value"] = request.value
    if request.direction is not None:
        args["direction"] = request.direction

    try:
        result = execute_tool(request.tool, args)
        return {
            "mode": "deterministic",
            "tool": request.tool,
            "args": args,
            "result": result,
        }
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {err}") from err


class ChemistrySolveRequest(BaseModel):
    solver_type: str = Field(..., description="Type of solver: stoichiometry, empirical_molecular, percent_composition, percent_error")
    show_work: bool = Field(False, description="Whether to include Ollama step-by-step explanation")
    
    # Stoichiometry parameters
    equation: Optional[str] = Field(None, description="Chemical equation")
    given_substance: Optional[str] = Field(None, description="Substance with known value")
    given_value: Optional[float] = Field(None, description="Known quantity")
    given_unit: Optional[str] = Field(None, description="grams, moles, liters, particles")
    target_substance: Optional[str] = Field(None, description="Substance to solve for")
    target_unit: Optional[str] = Field(None, description="grams, moles, liters, particles")
    
    # Empirical & Molecular parameters
    composition: Optional[Dict[str, float]] = Field(None, description="Element to percent composition/mass mapping")
    molar_mass: Optional[float] = Field(None, description="Optional molecular molar mass")
    
    # Percent Composition parameter
    formula: Optional[str] = Field(None, description="Chemical formula")
    
    # Percent Error parameters
    theoretical: Optional[float] = Field(None, description="Expected value")
    experimental: Optional[float] = Field(None, description="Measured value")


@router.post("/solve")
async def solve(request: ChemistrySolveRequest):
    """Run AI-assisted chemistry solver with deterministic validation and optional explanation."""
    try:
        if request.solver_type == "stoichiometry":
            if not all([request.equation, request.given_substance, request.given_value is not None, request.given_unit, request.target_substance, request.target_unit]):
                raise HTTPException(status_code=400, detail="Missing required parameters for stoichiometry solver.")
            
            result = await stoichiometry_solver.solve(
                show_work=request.show_work,
                equation=request.equation,
                given_substance=request.given_substance,
                given_value=request.given_value,
                given_unit=request.given_unit,
                target_substance=request.target_substance,
                target_unit=request.target_unit
            )
            return result

        elif request.solver_type == "empirical_molecular":
            if not request.composition:
                raise HTTPException(status_code=400, detail="Composition data is required for empirical/molecular formula solver.")
            
            result = await empirical_molecular_solver.solve(
                show_work=request.show_work,
                composition=request.composition,
                molar_mass=request.molar_mass
            )
            return result

        elif request.solver_type == "percent_composition":
            if not request.formula:
                raise HTTPException(status_code=400, detail="Chemical formula is required for percent composition solver.")
            
            result = await percent_composition_solver.solve(
                show_work=request.show_work,
                formula=request.formula
            )
            return result

        elif request.solver_type == "percent_error":
            if request.theoretical is None or request.experimental is None:
                raise HTTPException(status_code=400, detail="Theoretical and experimental values are required for percent error solver.")
            
            result = await percent_error_solver.solve(
                show_work=request.show_work,
                theoretical=request.theoretical,
                experimental=request.experimental
            )
            return result

        else:
            raise HTTPException(status_code=400, detail=f"Unknown solver type: {request.solver_type}")

    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err)) from val_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Solver error: {str(e)}") from e


@router.get("/search-kb")
def search_kb(query: str, category: Optional[str] = None):
    """Offline/online knowledge base search."""
    try:
        results = kb_search_index.search(query, category)
        suggestions = []
        if not results:
            suggestions = kb_search_index.suggest_corrections(query)
        return {
            "results": results,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}") from e
