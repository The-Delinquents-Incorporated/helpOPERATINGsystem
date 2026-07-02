from fastapi import APIRouter, HTTPException, Path
from typing import List, Union
from backend.app.core.periodic_table import get_element, list_all_elements, Element

router = APIRouter(prefix="/api/elements", tags=["Periodic Table"])

@router.get("", response_model=List[Element])
async def get_all_elements():
    """
    Retrieve all 118 periodic table elements ordered by atomic number.
    """
    return list_all_elements()

@router.get("/{query}", response_model=Element)
async def get_element_by_query(
    query: str = Path(..., description="Element symbol (e.g. H, He, Li), name, or atomic number")
):
    """
    Retrieve element details by atomic number, symbol, or name.
    """
    # Convert query to int if possible
    lookup_val: Union[str, int] = query
    if query.isdigit():
        lookup_val = int(query)
        
    element = get_element(lookup_val)
    if not element:
        raise HTTPException(
            status_code=404, 
            detail=f"Element '{query}' not found. Please specify a valid atomic number, symbol, or name."
        )
    return element
