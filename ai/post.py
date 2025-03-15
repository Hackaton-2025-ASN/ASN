from typing import Optional

from auto_id import AutoID


class Post(AutoID):
    def __init__(self, content: str, image: Optional[bytes] = None, id: Optional[int] = None):
        super().__init__(id=id)

        self.content = content
        self.image: Optional[bytes] = image

    def __str__(self):
        return f"Post(id={self.id}, content={self.content})" # TODO: add image
