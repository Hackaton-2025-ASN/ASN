from typing import Optional

from ai.auto_id import AutoID


class User(AutoID):
    def __init__(self, name: str, id: Optional[int] = None):
        super().__init__(id=id)
        self.name: str = name

    def __str__(self) -> str:
        return f"User(id={self.id}, name={self.name})"
