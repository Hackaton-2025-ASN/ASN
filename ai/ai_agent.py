from abc import ABC, abstractmethod
from typing import Optional, List

from auto_id import AutoID
from event import Event


class AIAgent(ABC, AutoID):
    def __init__(self, name: str, instructions: str, image: Optional[bytes] = None):
        super().__init__()

        self.name = name
        self.image: Optional[bytes] = image
        self.instructions: str = self._modify_instructions(instructions)

    @abstractmethod
    def react_on_events(self, events: List[Event]) -> Optional[List[Event]]:
        ...#TODO: implement this method
    @abstractmethod
    def _modify_instructions(self, instructions: str) -> str:
        return instructions # TODO: implement this method

    def _stringify_events(self, events: List[Event]) -> str:
        return "\n".join(str(event) for event in events)

    @abstractmethod
    def _prompt_model(self, prompt: str) -> Optional[str]:
        ...
