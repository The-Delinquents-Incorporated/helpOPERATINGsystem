from typing import Dict, Optional, List, Union
from pydantic import BaseModel

class Element(BaseModel):
    atomic_number: int
    symbol: str
    name: str
    mass: float
    is_isotope: bool

# Raw CDE Periodic Table Data
# (atomic_number, symbol, name, mass, is_isotope)
_RAW_ELEMENTS = [
    (1, "H", "hydrogen", 1.01, False),
    (2, "He", "helium", 4.00, False),
    (3, "Li", "lithium", 6.94, False),
    (4, "Be", "beryllium", 9.01, False),
    (5, "B", "boron", 10.81, False),
    (6, "C", "carbon", 12.01, False),
    (7, "N", "nitrogen", 14.01, False),
    (8, "O", "oxygen", 16.00, False),
    (9, "F", "fluorine", 19.00, False),
    (10, "Ne", "neon", 20.18, False),
    (11, "Na", "sodium", 22.99, False),
    (12, "Mg", "magnesium", 24.30, False),
    (13, "Al", "aluminum", 26.98, False),
    (14, "Si", "silicon", 28.09, False),
    (15, "P", "phosphorus", 30.97, False),
    (16, "S", "sulfur", 32.06, False),
    (17, "Cl", "chlorine", 35.45, False),
    (18, "Ar", "argon", 39.95, False),
    (19, "K", "potassium", 39.10, False),
    (20, "Ca", "calcium", 40.08, False),
    (21, "Sc", "scandium", 44.96, False),
    (22, "Ti", "titanium", 47.87, False),
    (23, "V", "vanadium", 50.94, False),
    (24, "Cr", "chromium", 52.00, False),
    (25, "Mn", "manganese", 54.94, False),
    (26, "Fe", "iron", 55.85, False),
    (27, "Co", "cobalt", 58.93, False),
    (28, "Ni", "nickel", 58.69, False),
    (29, "Cu", "copper", 63.55, False),
    (30, "Zn", "zinc", 65.38, False),
    (31, "Ga", "gallium", 69.72, False),
    (32, "Ge", "germanium", 72.63, False),
    (33, "As", "arsenic", 74.92, False),
    (34, "Se", "selenium", 78.97, False),
    (35, "Br", "bromine", 79.90, False),
    (36, "Kr", "krypton", 83.80, False),
    (37, "Rb", "rubidium", 85.47, False),
    (38, "Sr", "strontium", 87.62, False),
    (39, "Y", "yttrium", 88.91, False),
    (40, "Zr", "zirconium", 91.22, False),
    (41, "Nb", "niobium", 92.91, False),
    (42, "Mo", "molybdenum", 95.95, False),
    (43, "Tc", "technetium", 98.0, True),
    (44, "Ru", "ruthenium", 101.07, False),
    (45, "Rh", "rhodium", 102.91, False),
    (46, "Pd", "palladium", 106.42, False),
    (47, "Ag", "silver", 107.87, False),
    (48, "Cd", "cadmium", 112.41, False),
    (49, "In", "indium", 114.82, False),
    (50, "Sn", "tin", 118.71, False),
    (51, "Sb", "antimony", 121.76, False),
    (52, "Te", "tellurium", 127.60, False),
    (53, "I", "iodine", 126.90, False),
    (54, "Xe", "xenon", 131.29, False),
    (55, "Cs", "cesium", 132.91, False),
    (56, "Ba", "barium", 137.33, False),
    (57, "La", "lanthanum", 138.91, False),
    (58, "Ce", "cerium", 140.12, False),
    (59, "Pr", "praseodymium", 140.91, False),
    (60, "Nd", "neodymium", 144.24, False),
    (61, "Pm", "promethium", 145.0, True),
    (62, "Sm", "samarium", 150.36, False),
    (63, "Eu", "europium", 151.96, False),
    (64, "Gd", "gadolinium", 157.25, False),
    (65, "Tb", "terbium", 158.93, False),
    (66, "Dy", "dysprosium", 162.50, False),
    (67, "Ho", "holmium", 164.93, False),
    (68, "Er", "erbium", 167.26, False),
    (69, "Tm", "thulium", 168.93, False),
    (70, "Yb", "ytterbium", 173.05, False),
    (71, "Lu", "lutetium", 174.97, False),
    (72, "Hf", "hafnium", 178.49, False),
    (73, "Ta", "tantalum", 180.95, False),
    (74, "W", "tungsten", 183.84, False),
    (75, "Re", "rhenium", 186.21, False),
    (76, "Os", "osmium", 190.23, False),
    (77, "Ir", "iridium", 192.22, False),
    (78, "Pt", "platinum", 195.08, False),
    (79, "Au", "gold", 196.97, False),
    (80, "Hg", "mercury", 200.59, False),
    (81, "Tl", "thallium", 204.38, False),
    (82, "Pb", "lead", 207.21, False),
    (83, "Bi", "bismuth", 208.98, False),
    (84, "Po", "polonium", 209.0, True),
    (85, "At", "astatine", 210.0, True),
    (86, "Rn", "radon", 222.0, True),
    (87, "Fr", "francium", 223.0, True),
    (88, "Ra", "radium", 226.0, True),
    (89, "Ac", "actinium", 227.0, True),
    (90, "Th", "thorium", 232.04, False),
    (91, "Pa", "protactinium", 231.04, False),
    (92, "U", "uranium", 238.03, False),
    (93, "Np", "neptunium", 237.0, True),
    (94, "Pu", "plutonium", 244.0, True),
    (95, "Am", "americium", 243.0, True),
    (96, "Cm", "curium", 247.0, True),
    (97, "Bk", "berkelium", 247.0, True),
    (98, "Cf", "californium", 251.0, True),
    (99, "Es", "einsteinium", 252.0, True),
    (100, "Fm", "fermium", 257.0, True),
    (101, "Md", "mendelevium", 258.0, True),
    (102, "No", "nobelium", 259.0, True),
    (103, "Lr", "lawrencium", 266.0, True),
    (104, "Rf", "rutherfordium", 267.0, True),
    (105, "Db", "dubnium", 268.0, True),
    (106, "Sg", "seaborgium", 269.0, True),
    (107, "Bh", "bohrium", 270.0, True),
    (108, "Hs", "hassium", 269.0, True),
    (109, "Mt", "meitnerium", 278.0, True),
    (110, "Ds", "darmstadtium", 281.0, True),
    (111, "Rg", "roentgenium", 282.0, True),
    (112, "Cn", "copernicium", 285.0, True),
    (113, "Nh", "nihonium", 286.0, True),
    (114, "Fl", "flerovium", 289.0, True),
    (115, "Mc", "moscovium", 289.0, True),
    (116, "Lv", "livermorium", 293.0, True),
    (117, "Ts", "tennessine", 294.0, True),
    (118, "Og", "oganesson", 294.0, True)
]

ELEMENTS: Dict[str, Element] = {}
ELEMENTS_BY_ATOMIC_NUMBER: Dict[int, Element] = {}

for num, sym, name, mass, iso in _RAW_ELEMENTS:
    el = Element(
        atomic_number=num,
        symbol=sym,
        name=name,
        mass=mass,
        is_isotope=iso
    )
    ELEMENTS[sym.upper()] = el
    ELEMENTS_BY_ATOMIC_NUMBER[num] = el

def get_element(query: Union[str, int]) -> Optional[Element]:
    """
    Look up an element by atomic number, symbol, or name (case-insensitive).
    """
    if isinstance(query, int):
        return ELEMENTS_BY_ATOMIC_NUMBER.get(query)
    
    if isinstance(query, str):
        # Clean query
        q = query.strip()
        
        # Check if query is digits
        if q.isdigit():
            return ELEMENTS_BY_ATOMIC_NUMBER.get(int(q))
            
        # Check by symbol
        q_upper = q.upper()
        if q_upper in ELEMENTS:
            return ELEMENTS[q_upper]
            
        # Check by name
        q_lower = q.lower()
        for el in ELEMENTS_BY_ATOMIC_NUMBER.values():
            if el.name == q_lower:
                return el
                
    return None

def list_all_elements() -> List[Element]:
    """
    Returns elements ordered by atomic number.
    """
    return [ELEMENTS_BY_ATOMIC_NUMBER[i] for i in sorted(ELEMENTS_BY_ATOMIC_NUMBER.keys())]
