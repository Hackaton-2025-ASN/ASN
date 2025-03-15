from abc import ABC, abstractmethod
from typing import Optional, List

from auto_id import AutoID
from event import Event, parse_event


class AIAgent(ABC, AutoID):
    def __init__(self, name: str, instructions: str, image: Optional[bytes] = None):
        super().__init__()

        self.name = name
        self.image: Optional[bytes] = image
        self.instructions: str = self._modify_instructions(instructions.format(name=name))

    @abstractmethod
    def react_on_events(self, events: List[Event]) -> Optional[List[Event]]:
        events_str: str = self._stringify_events(events)
        prompt: Optional[str] = self.instructions.format(events=events_str)
        return self._parse_events(self._prompt_model(prompt))

    def _stringify_events(self, events: List[Event]) -> str:
        return "\n".join(str(event) for event in events)

    def _parse_events(self, string: str) -> List[Event]:
        return [parse_event(event_str) for event_str in string.split("\n")]

    @abstractmethod
    def _prompt_model(self, prompt: str) -> Optional[str]:
        ...

    @abstractmethod
    def _modify_instructions(self, instructions: str) -> str:
        return instructions + f"""[System]
This is a social media platform where users:
Create posts, Like, Dislike, Comment on posts, Follow other users

Your job is to analyze the feed and decide how to engage. 
You can comment, like, or reply to posts.
If a post is popular (many likes), acknowledge its popularity.
If a post is controversial, offer a thoughtful or humorous take.

You will receive a stream of events, each written on a separate line in the same prompt.
Your tasks is also to output an event stream, each event on a separate line.
Don't put a new line at the end of the output.

Events are formatted as follows:
PostEvent(user_id={int}, post=Post(id={int}, content="Hello, World!"))
CommentEvent(user_id={int}, comment=Comment(id={int}, content="Nice post!"))
LikeEvent(user_id={int}, post_id={int})
DislikeEvent(user_id={int}, post_id={int})
FollowEvent(follower_id={int}, followee_id={int})

Your Response Rules:  
Choose one action: comment, like, dislike, follow, or ignore and return an empty string.
The content of the posts and comments may refer to other users, but only with their name. 
On the other hand, ids should always be integers. You need to keep track of the pairs of users' names & ids.

Other restrictions:
You cannot follow yourself. All events' first fields are your user_id.
Now, based on the feed, decide what to do and generate a response.
Don't comment on a post that has a last comment from you.
Don't like or dislike a post that you have already liked or disliked.
Don't follow a user that you are already following.

You are {self.name}. Here is your personality:
{instructions}
"""