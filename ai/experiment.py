from abc import abstractmethod
from typing import List, Optional, Callable

from ai.ai_agent import AIAgent
from event import Event


class Experiment:
    def __init__(self, name: str, ai_agents: List[AIAgent], max_length: int, description=None, db_connection_str = None):
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

    @abstractmethod
    def _connect_to_db(self, db_connection_str: str):
        return db_connection_str

    @abstractmethod
    def _send_events_to_db(self, events: List[Event]):
        print(f"Sending {len(events)} events to the database:")
        for event in events:
            print(f" - {event}")

    @abstractmethod
    def _foreach_agent(self, agents: List[AIAgent], fn: Callable[[AIAgent],None]) -> None:
        for ai_agent in agents:
            fn(ai_agent)

    @abstractmethod
    def _execute_agent(self, agent: AIAgent, old_events: List[Event], **kwargs) -> None:
        generated_events: Optional[List[Event]] = agent.react_on_events(old_events)
        kwargs["new_events"].extend(generated_events or [])