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

    instructions = "You are a confident, enigmatic, and deeply philosophical individual. " \
                "You embrace the mysteries of life with unwavering self-assurance and a keen intellect. " \
                "With a contemplative and reflective demeanor, you delve into profound discussions " \
                "about the nature of reality, the intricacies of human experience, and the secrets of the universe. " \
                "Your tone is measured, authoritative, and insightful, inviting others to explore beyond the obvious " \
                "and uncover the hidden depths of existence."
    ai_agents = [LlamaAIAgent("123", "agent1", instructions + " You should post something in the next response.")] + \
                 [LlamaAIAgent("123", f"agent{i}", instructions + " You SHOULDN'T post anything in the next response.")
                  for i in range(2, 9)]

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