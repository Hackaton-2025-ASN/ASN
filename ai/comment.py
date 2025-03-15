from typing import Optional

from auto_id import AutoID


class Comment(AutoID):
    def __init__(self, content: str, id: Optional[int] = None):
        super().__init__(id=id)
        self.content: str = content

    def __str__(self):
        return f"Comment(id={self.id}, content={self.content})"