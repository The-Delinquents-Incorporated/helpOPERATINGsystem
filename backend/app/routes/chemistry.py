from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.coordinator import execute_tool

router = APIRouter(prefix="/api/chemistry", tags=["Chemistry"])


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
