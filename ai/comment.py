from typing import Optional

from .auto_id import AutoID


class Comment(AutoID):
    def __init__(self, post_id: int, content: str, id: Optional[int] = None):
        super().__init__(id=id)
        self.post_id: int = post_id
        self.content: str = content

    def __str__(self):
        return f"Comment(id={self.id}, post_id={self.post_id}, content={self.content})"
