import json
import os
import re
from typing import Dict, List, Any, Optional

# Strips LaTeX-style formatting characters (e.g. "H_2O", "SO_4^{2-}")
# so plain queries like "H2O" or "SO4" still match KB entries.
_LATEX_MARKUP = re.compile(r"[_^{}]")


def _plain(text: Any) -> str:
    return _LATEX_MARKUP.sub("", str(text or "")).lower()


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

        q = _plain(query.strip())
        results = []

        target_cats = [category] if category and category in self.categories else self.categories

        for cat in target_cats:
            items = self.data.get(cat, [])
            for item in items:
                matched = False
                # Match based on category fields. Formulas are stored with LaTeX
                # markup, so compare against their plain-text form.
                if cat == "elements":
                    matched = (
                        q in item.get("name", "").lower() or
                        q == item.get("symbol", "").lower() or
                        q == str(item.get("atomic_number", ""))
                    )
                elif cat == "compounds":
                    matched = (
                        q in item.get("name", "").lower() or
                        q in _plain(item.get("formula", "")) or
                        q in item.get("properties", "").lower()
                    )
                elif cat == "polyatomic_ions":
                    matched = (
                        q in item.get("name", "").lower() or
                        q in _plain(item.get("formula", "")) or
                        q == str(item.get("charge", ""))
                    )
                elif cat == "reaction_types":
                    matched = (
                        q in item.get("type", "").lower() or
                        q in _plain(item.get("pattern", "")) or
                        q in _plain(item.get("example", ""))
                    )

                if matched:
                    # Create a standard search result format
                    results.append({
                        "category": cat,
                        "data": item
                    })
        return results

    def suggest_corrections(self, typo: str) -> List[str]:
        # Simple fuzzy matching using substring/char overlap on plain-text forms
        if not typo:
            return []
        typo_l = _plain(typo)
        candidates = []

        # Gather all names and formulas
        for cat, items in self.data.items():
            for item in items:
                names = [item.get("name", ""), item.get("symbol", ""), item.get("formula", ""), item.get("type", "")]
                for name in names:
                    if name:
                        nl = _plain(name)
                        # standard check: prefix or substring
                        if typo_l in nl or nl in typo_l:
                            candidates.append(name)
        return list(set(candidates))[:5]
