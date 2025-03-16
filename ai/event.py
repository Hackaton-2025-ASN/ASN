from abc import ABC, abstractmethod
from typing import Optional, Tuple

from ai.utils import extract_placeholders
from .auto_id import AutoID
from .comment import Comment
from .post import Post


Tup = Tuple[int, Optional[int], Optional[str], Optional[str], Optional[bytes], Optional[int], Optional[str], Optional[str]]

class Event(ABC, AutoID):

    def __init__(self, id: Optional[int] = None):
        super().__init__(id=id)

    @abstractmethod
    def __str__(self) -> str:
        ...

    @classmethod
    def from_string(cls, string: str, user_id: str) -> 'Event':
        ...

    def to_tuple(self) -> Tup:
        ...


class PostEvent(Event):
    def __init__(self, user_id: str, post: Post, id: Optional[int] = None):
        super().__init__(id=id)
        self.user_id: str = user_id
        self.post: Post = post

    def __str__(self) -> str:
        return f"PostEvent(user_id={self.user_id}, post={self.post})"

    @classmethod
    def from_string(cls, string: str, user_id: str) -> 'PostEvent':
        groups_event = extract_placeholders("PostEvent(user_id={user_id}, post={post})", string)

        if not groups_event:
            raise ValueError(f"Invalid PostEvent string: {string}")

        groups_post = extract_placeholders("Post(id={id}, content={content})", groups_event["post"])

        if not groups_post:
            raise ValueError(f"Invalid PostEvent string: {string}")

        try:
            post = Post(content=groups_post["content"])

            return PostEvent(user_id=user_id, post=post)
        except ValueError as e:
            print(string)
            raise ValueError(f"Invalid PostEvent string: {string}") from e

    def to_tuple(self) -> Tup:
        return (
            self.id,
            1,
            self.user_id,
            self.post.id,
            self.post.content,
            self.post.image,
            None,
            None
        )



class CommentEvent(Event):
    def __init__(self, user_id: str, comment: Comment, id: Optional[int] = None):
        super().__init__(id=id)
        self.user_id: str = user_id
        self.comment: Comment = comment

    def __str__(self) -> str:
        return f"CommentEvent(user_id={self.user_id}, comment={self.comment})"

    @classmethod
    def from_string(cls, string: str, user_id: str) -> 'CommentEvent':
        groups_event = extract_placeholders("CommentEvent(user_id={user_id}, comment={comment})", string)

        if not groups_event:
            raise ValueError(f"Invalid CommentEvent string: {string}")

        groups_comment = extract_placeholders(
            "Comment(id={id}, post_id={post_id}, content={content})",
            groups_event["comment"]
        )

        if not groups_comment:
            raise ValueError(f"Invalid CommentEvent string: {string}")

        try:
            comment = Comment(post_id=int(groups_comment["post_id"]), content=groups_comment["content"])

            return CommentEvent(user_id=user_id, comment=comment)
        except ValueError as e:
            raise ValueError(f"Invalid CommentEvent string: {string}") from e

    def to_tuple(self) -> Tup:
        return (
            self.id,
            2,
            self.user_id,
            self.comment.id,
            self.comment.content,
            None,
            None,
            None
        )


class LikeEvent(Event):
    def __init__(self, user_id: str, post_id: int, id: Optional[int] = None):
        super().__init__(id=id)
        self.user_id: str = user_id
        self.post_id: int = post_id

    def __str__(self) -> str:
        return f"LikeEvent(user_id={self.user_id}, post_id={self.post_id})"

    @classmethod
    def from_string(cls, string: str, user_id: str) -> 'LikeEvent':
        groups_event = extract_placeholders("LikeEvent(user_id={user_id}, post_id={post_id})", string)

        if not groups_event:
            raise ValueError(f"Invalid LikeEvent string: {string}")

        try:
            return LikeEvent(user_id=user_id, post_id=int(groups_event["post_id"]))
        except ValueError as e:
            raise ValueError(f"Invalid LikeEvent string: {string}") from e

    def to_tuple(self) -> Tup:
        return (
            self.id,
            3,
            self.user_id,
            self.post_id,
            None,
            None,
            None,
            None
        )


class DislikeEvent(Event):
    def __init__(self, user_id: str, post_id: int, id: Optional[int] = None):
        super().__init__(id=id)
        self.user_id: str = user_id
        self.post_id: int = post_id

    def __str__(self) -> str:
        return f"DislikeEvent(user_id={self.user_id}, post_id={self.post_id})"

    @classmethod
    def from_string(cls, string: str, user_id: str) -> 'DislikeEvent':
        groups_event = extract_placeholders("DislikeEvent(user_id={user_id}, post_id={post_id})", string)

        if not groups_event:
            raise ValueError(f"Invalid DislikeEvent string: {string}")

        try:
            return DislikeEvent(user_id=user_id, post_id=int(groups_event["post_id"]))
        except ValueError as e:
            raise ValueError(f"Invalid DislikeEvent string: {string}") from e

    def to_tuple(self) -> Tup:
        return (
            self.id,
            4,
            self.user_id,
            self.post_id,
            None,
            None,
            None,
            None
        )


class FollowEvent(Event):
    def __init__(self, follower_id: str, followee_id: str):
        super().__init__()
        self.follower_id: str = follower_id
        self.followee_id: str = followee_id

    def __str__(self) -> str:
        return f"FollowEvent(follower_id={self.follower_id}, followee_id={self.followee_id})"

    @classmethod
    def from_string(cls, string: str, user_id: str) -> 'FollowEvent':
        groups_event = extract_placeholders("FollowEvent(follower_id={follower_id}, followee_id={followee_id})", string)

        if not groups_event:
            raise ValueError(f"Invalid FollowEvent string: {string}")

        try:
            return FollowEvent(follower_id=user_id, followee_id=groups_event["followee_id"])
        except ValueError as e:
            raise ValueError(f"Invalid FollowEvent string: {string}") from e

    def to_tuple(self) -> Tup:
        return (
            self.id,
            5,
            None,
            None,
            None,
            None,
            self.follower_id,
            self.followee_id
        )


def parse_event(string: str, user_id: str) -> Event:
    event_type: str = string.split("(")[0]
    for event_cls in Event.__subclasses__():
        if event_cls.__name__ == event_type:
            return event_cls.from_string(string, user_id)

    raise ValueError(f"Invalid event string: {string}")
