from abc import ABC, abstractmethod
from typing import Optional, List

from auto_id import AutoID
from event import Event, parse_event, FollowEvent


class AIAgent(ABC, AutoID):
    def __init__(self, experiment_id: str, name: str, instructions: str, image: Optional[bytes] = None):
        super().__init__()
        self.experiment_id: str = experiment_id
        self.name: str = name
        self.image: Optional[bytes] = image
        self.instructions: str = instructions
        self.user_db: str = ""

    def add_user_db(self, user_db: str):
        self.user_db = user_db

    def prepare(self):
        self.instructions: str = self._modify_instructions(self.instructions)

    def react_on_events(self, events: List[Event]) -> Optional[List[Event]]:
        events_str: str = self._stringify_events(events)
        prompt: str = self.instructions + events_str
        result: Optional[str] = self._prompt_model(prompt)
        events = self._parse_events(result) if result else None
        events = self.filter_invalid_events(events) if events else None
        return events

    def _stringify_events(self, events: List[Event]) -> str:
        return "\n".join(str(event) for event in events)

    def _parse_events(self, string: str) -> List[Event]:
        result = []
        for event_str in string.split("\n"):
            try:
                result.append(parse_event(event_str, self.id))
            except ValueError:
                pass

        return result

    def filter_invalid_events(self, events: List[Event]) -> List[Event]:
        return [event for event in events if not (isinstance(event, FollowEvent) and
                                                  event.follower_id == event.followee_id)]

    def _prompt_model(self, prompt: str) -> Optional[str]:
        ...

    def _modify_instructions(self, instructions: str) -> str:
        return f"""1. Role
You are {self.name}, a person in a social media. Follow these special instructions: {instructions}. 
Interact with others by posting, commenting, liking/disliking, or following—always reflecting your unique background.

2. Task
You'll receive a stream of events (one per line) describing user or your previous actions. For each line, respond with 
preferable one event (or an empty line to ignore, or more than 2) using the strict formats below.

3. Format & Rules
PostEvent(user_id={{int}}, post=Post(id={{int}}, content={{string}}))
CommentEvent(user_id={{int}}, comment=Comment(id={{int}}, post_id={{int}}, content={{string}}))
LikeEvent(user_id={{int}}, post_id={{int}})
DislikeEvent(user_id={{int}}, post_id={{int}})
FollowEvent(follower_id={{int}}, followee_id={{int}})

4. Identity
User Database: {self.user_db}. You are {self.name} with id: {self.id}.

Example:
Input:
  PostEvent(user_id=2, post=Post(id=101, content=Hello!))
  LikeEvent(user_id=3, post_id=101)
Output:
  CommentEvent(user_id={self.id}, comment=Comment(id=301, post_id=101, content=Hi from {self.name}!))

"""