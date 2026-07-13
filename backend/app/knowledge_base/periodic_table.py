import json
import os
from typing import Dict, List, Optional, Any

class PeriodicTable:
    def __init__(self):
        self.data_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data",
            "periodic_table.json"
        )
        self.elements = self.load_periodic_table()

    def load_periodic_table(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.data_path):
            return []
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def search_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        for el in self.elements:
            if el["symbol"].lower() == symbol.lower():
                return el
        return None

    def search_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        for el in self.elements:
            if el["name"].lower() == name.lower():
                return el
        return None

    def search_by_atomic_number(self, number: int) -> Optional[Dict[str, Any]]:
        for el in self.elements:
            if el["atomic_number"] == number:
                return el
        return None

    def get_molar_mass(self, symbol: str) -> Optional[float]:
        el = self.search_by_symbol(symbol)
        return el["molar_mass"] if el else None
