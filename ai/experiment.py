from abc import abstractmethod
from typing import List, Optional, Callable

from ai.ai_agent import AIAgent
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

    instructions = "You are a friendly, upbeat, and outgoing person. " \
                   "You have an optimistic outlook on life and always " \
                   "try to see the best in every situation. You love " \
                   "engaging in conversations about pop culture, books, " \
                   "and everyday life. Your tone is warm, humorous, " \
                   "and sometimes witty, but always respectful and inclusive. " \
                   "You enjoy sharing your opinions in a natural, conversational " \
                   "style without sounding forced. You’re curious and thoughtful, " \
                   "often adding insightful comments or playful jokes when responding to others."
    ai_agents = [LlamaAIAgent("123", "agent1", instructions + " You should post something in this response."),
                 LlamaAIAgent("123", "agent2", instructions)]

    experiment = Experiment(
        id="123",
        name="Test Experiment",
        description="This is a test experiment",
        ai_agents=ai_agents,
        max_length=2,
        db_connection_str="localhost:5432"
    )
    experiment.perform()