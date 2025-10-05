# facts.py
# Purpose: Load and serve random "fun facts" with session-aware de-duplication.
# Storage choice: simple JSON file loaded into memory. No database needed for this scope.

from __future__ import annotations
import json
import os
import random
from typing import List, Dict, Tuple

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "facts.json")

class Facts:
    def __init__(self) -> None:
        self._facts: List[str] = []
        self._load()

    def _load(self) -> None:
        """Load facts from JSON. Fallback to a safe built-in list if file is missing or invalid."""
        fallback = [
            # Guayaquil
            "Guayaquil is Ecuador’s largest city and main seaport.",
            "The Malecón 2000 is a riverfront walkway along the Guayas River in Guayaquil.",
            "Parque Seminario in Guayaquil is known as Iguana Park.",
            "José Joaquín de Olmedo International Airport serves Guayaquil.",
            "Las Peñas is a historic hillside neighborhood with colorful houses.",
            "Guayaquil sits near the Gulf of Guayaquil on the Pacific.",
            "Guayaquil has a tropical, humid climate.",
            "The Daule and Babahoyo rivers meet near Guayaquil to form the Guayas River.",
            # Dogs
            "Chocolate is unsafe for dogs.",
            "Dogs cool themselves mainly by panting.",
            "A wagging tail can signal many emotions, not only happiness.",
            "Microchips improve the chances of finding a lost dog.",
            "Grapes and raisins are unsafe for dogs.",
            "Ask the owner before petting an unfamiliar dog.",
            "Daily exercise and simple games help most dogs stay calm.",
            "Clean, fresh water is essential for dogs at all times.",
        ]

        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if not isinstance(payload, dict):
                self._facts = fallback
                return
            merged: List[str] = []
            for key in ("guayaquil", "dogs"):
                items = payload.get(key, [])
                if isinstance(items, list):
                    merged.extend([str(x).strip() for x in items if str(x).strip()])
            # Ensure we have content
            self._facts = merged if merged else fallback
        except Exception:
            # On any parsing or IO error, use fallback
            self._facts = fallback

    def all(self) -> List[str]:
        return list(self._facts)

    def pick_unique(self, seen: List[int]) -> Tuple[int, str]:
        """Pick a random fact index not in 'seen'. If exhausted, reset seen and pick again."""
        total = len(self._facts)
        if total == 0:
            return -1, "No facts available."
        # Build pool of available indices
        available = [i for i in range(total) if i not in set(seen)]
        if not available:
            # Reset logic: if all seen, start from fresh
            available = list(range(total))
        idx = random.choice(available)
        return idx, self._facts[idx]


FACTS = Facts()
