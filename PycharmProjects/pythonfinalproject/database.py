"""Database model for persisting leagues to/from JSON."""

import json
from typing import List
from .league import League


class Database:
    """Manages a collection of leagues and handles serialization."""

    def __init__(self):
        self._leagues: List[League] = []

    @property
    def leagues(self) -> List[League]:
        return list(self._leagues)

    def add_league(self, league: League):
        self._leagues.append(league)

    def remove_league(self, index: int):
        if 0 <= index < len(self._leagues):
            del self._leagues[index]
        else:
            raise IndexError(f"League index {index} out of range.")

    def clear(self):
        self._leagues.clear()

    def to_dict(self) -> dict:
        return {"leagues": [lg.to_dict() for lg in self._leagues]}

    @classmethod
    def from_dict(cls, data: dict) -> "Database":
        db = cls()
        for lg_data in data.get("leagues", []):
            db.add_league(League.from_dict(lg_data))
        return db

    def save(self, filepath: str):
        """Save the database to a JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "Database":
        """Load a database from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __len__(self) -> int:
        return len(self._leagues)
