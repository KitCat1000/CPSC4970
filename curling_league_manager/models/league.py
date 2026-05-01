"""
Nicole Tressler
April 21, 2026.
CPSC 4970, Auburn University

Final Project: PyQt5 Interface

"""


"""League model representing a curling league."""

from typing import List
from .team import Team


class League:
    """Represents a curling league containing teams."""

    def __init__(self, name: str):
        if not name or not name.strip():
            raise ValueError("League name cannot be empty.")
        self._name = name.strip()
        self._teams: List[Team] = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("League name cannot be empty.")
        self._name = value.strip()

    @property
    def teams(self) -> List[Team]:
        return list(self._teams)

    def add_team(self, team: Team):
        self._teams.append(team)

    def remove_team(self, index: int):
        if 0 <= index < len(self._teams):
            del self._teams[index]
        else:
            raise IndexError(f"Team index {index} out of range.")

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "teams": [t.to_dict() for t in self._teams],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "League":
        league = cls(name=data.get("name", "Unnamed League"))
        for t_data in data.get("teams", []):
            league.add_team(Team.from_dict(t_data))
        return league

    def __repr__(self) -> str:
        return f"League(name={self._name!r}, teams={len(self._teams)})"

    def __str__(self) -> str:
        return self._name
