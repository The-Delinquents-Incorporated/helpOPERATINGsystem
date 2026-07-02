import pytest
from backend.app.core.periodic_table import get_element, list_all_elements

def test_periodic_table_completeness():
    elements = list_all_elements()
    assert len(elements) == 118
    
    # Check that they are ordered 1 to 118
    for idx, el in enumerate(elements):
        assert el.atomic_number == idx + 1

def test_cast_specific_element_masses():
    # Hydrogen
    h = get_element("H")
    assert h is not None
    assert h.name == "hydrogen"
    assert h.mass == 1.01
    assert h.is_isotope is False

    # Carbon
    c = get_element("C")
    assert c is not None
    assert c.mass == 12.01
    assert c.is_isotope is False

    # Oxygen
    o = get_element("O")
    assert o is not None
    assert o.mass == 16.00
    assert o.is_isotope is False

    # Technetium (isotope)
    tc = get_element("Tc")
    assert tc is not None
    assert tc.mass == 98.0
    assert tc.is_isotope is True

    # Iodine
    i = get_element("I")
    assert i is not None
    assert i.mass == 126.90
    assert i.is_isotope is False

    # Uranium
    u = get_element("U")
    assert u is not None
    assert u.mass == 238.03
    assert u.is_isotope is False

    # Oganesson (isotope)
    og = get_element("Og")
    assert og is not None
    assert og.mass == 294.0
    assert og.is_isotope is True

def test_get_element_variants():
    # Test case insensitivity for symbol
    assert get_element("he") == get_element("He")
    assert get_element("HE") == get_element("He")
    
    # Test case insensitivity for name
    assert get_element("helium") == get_element("He")
    assert get_element("HELIUM") == get_element("He")
    assert get_element(" Helium ") == get_element("He")
    
    # Test by atomic number (int and str)
    assert get_element(2) == get_element("He")
    assert get_element("2") == get_element("He")

def test_get_element_not_found():
    assert get_element("X") is None
    assert get_element(119) is None
    assert get_element("119") is None
    assert get_element("invalid") is None
