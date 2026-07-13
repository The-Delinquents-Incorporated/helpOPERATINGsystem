import json
import os
from typing import Dict, List, Any, Optional

class KBSearch:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.categories = ["elements", "compounds", "polyatomic_ions", "reaction_types"]
        self.data = self._load_all_data()

    def _load_all_data(self) -> Dict[str, List[Any]]:
        loaded = {}
        for cat in self.categories:
            path = os.path.join(self.base_dir, "data", f"{cat if cat != 'elements' else 'periodic_table'}.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    loaded[cat] = json.load(f)
            else:
                loaded[cat] = []
        return loaded

    def search(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        if not query:
            return []
        
        q = query.lower().strip()
        results = []

        target_cats = [category] if category and category in self.categories else self.categories

        for cat in target_cats:
            items = self.data.get(cat, [])
            for item in items:
                matched = False
                # Match based on category fields
                if cat == "elements":
                    matched = (
                        q in item.get("name", "").lower() or
                        q == item.get("symbol", "").lower() or
                        q == str(item.get("atomic_number", ""))
                    )
                elif cat == "compounds":
                    matched = (
                        q in item.get("name", "").lower() or
                        q in item.get("formula", "").lower() or
                        q in item.get("properties", "").lower()
                    )
                elif cat == "polyatomic_ions":
                    matched = (
                        q in item.get("name", "").lower() or
                        q in item.get("formula", "").lower() or
                        q == str(item.get("charge", ""))
                    )
                elif cat == "reaction_types":
                    matched = (
                        q in item.get("type", "").lower() or
                        q in item.get("pattern", "").lower() or
                        q in item.get("example", "").lower()
                    )

                if matched:
                    # Create a standard search result format
                    results.append({
                        "category": cat,
                        "data": item
                    })
        return results

    def suggest_corrections(self, typo: str) -> List[str]:
        # Simple fuzzy matching using Levenshtein distance or simple substring/char overlap
        if not typo:
            return []
        typo_l = typo.lower()
        candidates = []
        
        # Gather all names and formulas
        for cat, items in self.data.items():
            for item in items:
                names = [item.get("name", ""), item.get("symbol", ""), item.get("formula", ""), item.get("type", "")]
                for name in names:
                    if name:
                        nl = name.lower()
                        # standard check: prefix or substring
                        if typo_l in nl or nl in typo_l:
                            candidates.append(name)
        return list(set(candidates))[:5]
