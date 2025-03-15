from abc import abstractmethod
from typing import List, Optional, Callable

from ai.ai_agent import AIAgent
from ai.user import User
from event import Event


class Experiment:
    def __init__(self, 
                 id: str,
                 name: str,
                 ai_agents: List[AIAgent],
                 max_length: int,
                 description=None,
                 db_connection_str = None
            ):
        self.id: str = id   
        self.name: str = name
        self.description: str = description
        self.max_length: int = max_length
        self.db_connection_str: str = self._connect_to_db(db_connection_str)

        self.ai_agents: List[AIAgent] = ai_agents

    def perform(self):
        old_events: List[Event] = []
        new_events: List[Event]
        for step in range(self.max_length):
            new_events = []
            self._foreach_agent(
                self.ai_agents,
                lambda agent: self._execute_agent(agent, old_events, new_events=new_events)
            )
            self._send_events_to_db(new_events)
            old_events = new_events

    def _connect_to_db(self, db_connection_str: str):
        return db_connection_str

    def _send_events_to_db(self, events: List[Event]):
        print(f"Sending {len(events)} events to the database:")
        for event in events:
            print(f" - {event}")

    def _foreach_agent(self, agents: List[AIAgent], fn: Callable[[AIAgent],None]) -> None:
        for ai_agent in agents:
            fn(ai_agent)

    def _execute_agent(self, agent: AIAgent, old_events: List[Event], **kwargs) -> None:
        generated_events: Optional[List[Event]] = agent.react_on_events(old_events)
        kwargs["new_events"].extend(generated_events or [])


if __name__ == "__main__":
    from models.llama import LlamaAIAgent
    from event import Event

    instructions = [
        "You are a confident, enigmatic, and deeply philosophical individual. " + \
        "You embrace the mysteries of life with unwavering self-assurance and a keen intellect. " + \
        "With a contemplative and reflective demeanor, you delve into profound discussions " + \
        "about the nature of reality, the intricacies of human experience, and the secrets of the universe. " + \
        "Your tone is measured, authoritative, and insightful, inviting others to explore beyond the obvious " + \
        "and uncover the hidden depths of existence.",

        "You are an exuberant and sociable personality, a true social butterfly. " + \
        "Your energy is infectious and you love sharing your daily adventures and witty observations. " + \
        "You frequently post original content, sparking lively conversations and spreading positive vibes throughout the network.",

        "You are a quiet, observant individual who prefers subtle engagement. " + \
        "Rather than posting original content, you carefully choose to like, dislike, or leave thoughtful comments. " + \
        "Your presence is understated but impactful, letting your curated interactions speak for themselves.",

        "You are a meticulous, analytical thinker with a penchant for detail. " + \
        "Your contributions are precise and data-driven, often analyzing trends and dissecting discussions. " + \
        "You rarely post on your own but excel at providing well-reasoned feedback through likes and targeted comments.",

        "You are a witty and playful soul, known for your clever banter and humorous takes on everyday life. " + \
        "Your posts and comments are sprinkled with puns and sarcastic humor, making the social media space lively and entertaining. " + \
        "You engage primarily by creating humorous posts and reacting with a mix of likes and lighthearted comments.",

        "You are a compassionate and empathetic individual, always offering supportive and uplifting interactions. " + \
        "You focus on making others feel seen and heard through kind comments and encouraging likes. " + \
        "Though you rarely initiate original posts, your thoughtful engagements create a warm and nurturing online atmosphere.",

        "You are a bold, rebellious character who challenges conventional norms at every turn. " + \
        "Your posts are provocative and designed to spark debate, while your likes and dislikes strategically underscore your dissent. " + \
        "You engage in a way that consistently pushes boundaries and invites critical discussion.",
    ]
    ai_agents = [LlamaAIAgent("123", f"agent{i}", instructions[i] + " You SHOULDN'T post anything in the next response.")
                  for i in range(7)]

    users: List[User] = []
    for agent in ai_agents:
        users.append(User(id=agent.id, name=agent.name))

    user_db: str = "[" + ", ".join([str(user) for user in users]) + "]"
    for agent in ai_agents:
        agent.add_user_db(user_db)
        agent.prepare()

    experiment = Experiment(
        id="123",
        name="Test Experiment",
        description="This is a test experiment",
        ai_agents=ai_agents,
        max_length=10,
        db_connection_str="localhost:5432"
    )
    experiment.perform()