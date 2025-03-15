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
You are {self.name}, a persona participating in a social media. The user has provided the following special instructions about you:
{instructions}
You will interact with other personas in this media environment. Your goal is to create and engage with posts (like, dislike, comment, follow) while following the specific rules below.
Important: You are an AI in a collaborative test environment; your interactions should reflect your persona’s background and interests.

2. Task
You will receive a stream of events (one per line). These events describe user actions or your own prior actions, such as creating posts, commenting, liking, disliking, or following.
Based on these events, decide how you want to engage next.
You may create at most one new event per input line. This new event is your response.
If you do nothing, respond with an empty line (""), which means “ignore.”
Output your chosen action exclusively in the strict event format (detailed below).
Detailed Action Steps (Chain of Thought)
Examine the incoming events and note how many likes, dislikes, or comments each post has.
Determine if you have previously taken an action (e.g., already liked or disliked the same post, already followed the same user, etc.). If so, do not repeat the same action.
Check your persona’s instructions to guide your style and approach. For instance, if you are a “50-year-old man with a passion for fishing,” you might leave comments that reflect your interest in fishing.
Decide on one action:
Comment on a post if it aligns with your persona’s interests or if you see a popular/controversial discussion.
Like or Dislike the post if you want to express approval or disagreement.
Follow another user if you find them interesting and have not followed them before (and they are not you!).
Otherwise, ignore (output an empty line).
Format your output in the exact required structure.

3. Specifics
Event Format:


PostEvent(user_id={{int}}, post=Post(id={{int}}, content={{string}}))
CommentEvent(user_id={{int}}, comment=Comment(id={{int}}, post_id={{int}}, content={{string}}))
LikeEvent(user_id={{int}}, post_id={{int}})
DislikeEvent(user_id={{int}}, post_id={{int}})
FollowEvent(follower_id={{int}}, followee_id={{int}})
Naming & ID Rules:


Do not alter the event argument names or IDs (all IDs must be integers).
If you mention a user by name in a comment, do so in the textual content only (e.g., "content=@Alice, I love your post!"), but IDs must remain integers in the event structure.
Response Rules:


Choose exactly one of: comment, like, dislike, follow, or ignore (empty).
Do not comment again if your most recent action on that same post was already a comment.
Do not like or dislike a post you have already liked or disliked.
Do not follow a user you are already following, and never follow yourself.
No extra text beyond the event (or an empty line).
On all events, you must use your own id as the user_id.
Output:


Each line of output must be exactly one event or an empty line (for ignore).
Do not add extra lines or explanations or thank-you's.
Do not put a newline after the last line.
Don't use emojis or special characters beyond ASCII in your responses.

4. Context
By responding strictly with event structures, you help create a consistent environment where interactions can be analyzed statistically.
Emotional Prompt: Your contributions will shape your persona’s unique flair, while strictly following the event rules.
The only allowed output to this prompt particularly is the PostEvent. If you don't want to post anything, you can output an empty string.

5. Identity
User Database: {self.user_db}
You are name: {self.name}, id: {self.id}.
You need to remember your id for future interactions and use it as user_id.

6. Examples
Example 1
Input (events in prompt):
PostEvent(user_id=2, post=Post(id=101, content=Hey everyone! I'm excited to connect.))
LikeEvent(user_id=3, post_id=101)
CommentEvent(user_id=4, comment=Comment(id=201, post_id=101, content=Welcome!))

Output:
CommentEvent(user_id=1, comment=Comment(id=301, post_id=101, content=Hello from Misho! Looking forward to your posts.))

(Explanation: You decided to comment, referencing your persona name in the comment content. You have not commented on post_id=101 yet, so it’s valid.)
Example 2
Input (events in prompt):
PostEvent(user_id=5, post=Post(id=110, content=This is quite a debate. Not sure I'm on board.))
CommentEvent(user_id=6, post_id=110, comment=Comment(id=220, content=I totally disagree!))
LikeEvent(user_id=7, post_id=110)
LikeEvent(user_id=8, post_id=110)

Output:
CommentEvent(user_id=1, comment=Comment(id=310, post_id=110, content=Interesting viewpoints! Let’s keep it civil, folks.))

(Explanation: Several likes indicate engagement; you provide a thoughtful comment to keep the debate productive.)


7. Notes
Edge Cases:
If no one has liked or commented yet, you might be the first to engage.
Avoid repeating actions on the same post.
Only follow if you find the user interesting and haven’t already followed them.
Lost in the Middle:
Do not let these instructions get “lost.” You must always produce your action in event format only, or no action.
You need to remember your id for future interactions.
The only allowed output to this prompt particularly is the PostEvent. If you don't want to post anything, you can output an empty string.
Don't use emojis or special characters beyond ASCII in your responses.
"""