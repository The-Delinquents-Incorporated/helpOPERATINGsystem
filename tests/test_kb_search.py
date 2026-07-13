import pytest
from backend.app.knowledge_base import KBSearch

def test_kb_search_element():
    search_idx = KBSearch()
    res = search_idx.search(query="Hydrogen")
    assert len(res) > 0
    assert res[0]["category"] == "elements"
    assert res[0]["data"]["symbol"] == "H"

def test_kb_search_compound():
    search_idx = KBSearch()
    res = search_idx.search(query="NaCl")
    assert len(res) > 0
    assert res[0]["category"] == "compounds"
    assert res[0]["data"]["name"] == "Sodium Chloride"

def test_kb_search_typo_suggestions():
    search_idx = KBSearch()
    res = search_idx.search(query="Hydr")
    assert len(res) > 0
    
    # Check typo suggestions for non-existent queries
    suggestions = search_idx.suggest_corrections(typo="Hydrog")
    assert "Hydrogen" in suggestions
