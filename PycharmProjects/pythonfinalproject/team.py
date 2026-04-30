"""Team model representing a curling team."""

from typing import List
from .member import Member


class Team:
    """Represents a curling team with a list of members."""

    def __init__(self, name: str):
        if not name or not name.strip():
            raise ValueError("Team name cannot be empty.")
        self._name = name.strip()
        self._members: List[Member] = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Team name cannot be empty.")
        self._name = value.strip()

    @property
    def members(self) -> List[Member]:
        return list(self._members)

    def add_member(self, member: Member):
        self._members.append(member)

    def remove_member(self, index: int):
        if 0 <= index < len(self._members):
            del self._members[index]
        else:
            raise IndexError(f"Member index {index} out of range.")

    def update_member(self, index: int, name: str, email: str):
        if 0 <= index < len(self._members):
            self._members[index].name = name
            self._members[index].email = email
        else:
            raise IndexError(f"Member index {index} out of range.")

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "members": [m.to_dict() for m in self._members],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Team":
        team = cls(name=data.get("name", "Unnamed Team"))
        for m_data in data.get("members", []):
            team.add_member(Member.from_dict(m_data))
        return team

    def __repr__(self) -> str:
        return f"Team(name={self._name!r}, members={len(self._members)})"

    def __str__(self) -> str:
        return self._name
