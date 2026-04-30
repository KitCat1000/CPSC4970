"""Member model representing a curling team member."""


class Member:
    """Represents a member of a curling team."""

    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Member name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value.strip() if value else ""

    def to_dict(self) -> dict:
        return {"name": self._name, "email": self._email}

    @classmethod
    def from_dict(cls, data: dict) -> "Member":
        return cls(name=data.get("name", ""), email=data.get("email", ""))

    def __repr__(self) -> str:
        return f"Member(name={self._name!r}, email={self._email!r})"

    def __str__(self) -> str:
        return f"{self._name} <{self._email}>" if self._email else self._name
