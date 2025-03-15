from typing import Optional

from ai.auto_id import AutoID


class User(AutoID):
    def __init__(self, user_id: int, name: str, id: Optional[int]=None):
        super().__init__(id=id)
        self.user_id: int = user_id
        self.name: str = name