from abc import ABC, abstractmethod

from auto_id import AutoID
from comment import Comment
from post import Post


class Event(ABC, AutoID):

    @abstractmethod
    def __str__(self) -> str:
        ...

    @classmethod
    def from_string(cls, string: str) -> 'Event':
        ...


class PostEvent(Event):
    def __init__(self, user_id: int, post: Post):
        super().__init__()
        self.user_id: int = user_id
        self.post: Post = post

    def __str__(self) -> str:
        return f"PostEvent(user_id={self.user_id}, post={self.post})"


class CommentEvent(Event):
    def __init__(self, user_id: int, comment: Comment):
        super().__init__()
        self.user_id: int = user_id
        self.post: Post = post

    def __str__(self) -> str:
        return f"CommentEvent(user_id={self.user_id}, post={self.post})"

class LikeEvent(Event):
    def __init__(self, user_id: User, post_id: Post):
        super().__init__()
        self.user_id: int = user_id
        self.post_id: int = post_id

    def __str__(self) -> str:
        return f"Event(user_id=\"User {self.user_id} liked post {self.post_id}\")"




class DislikeEvent(Event):
    def __init__(self, user_id: int, post_id: int):
        super().__init__()
        self.user_id: int = user_id
        self.post_id: int = post_id

    def __str__(self) -> str:
        return f"Event(\"User {self.user_id} disliked post {self.post_id}\")"


class FollowEvent(Event):
    def __init__(self, follower_id: int, followee_id: int):
        super().__init__()
        self.follower_id: int = follower_id
        self.followee_id: int = followee_id

    def __str__(self) -> str:
        return f"Event(\"User {self.user_id} followed post {self.post_id}\")"