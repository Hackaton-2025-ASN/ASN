import os
from typing import List

import openai
from pymongo import MongoClient
from bson import ObjectId

from ai.ai_agent import AIAgent
from ai.event import Event
from ai.models.gpt_agent import GPT4AIAgent


class DBProxy:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONG_DB_CONN"))

    def insert_event_batch(self, events: List[Event]):
        db = self.client["eventstreams"]
        db.events.insert_many([event for event in events])

    def get_ai_agents(self, experiment_id: str) -> List[AIAgent]:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        db = self.client.get_database("test")

        result = list(db["agents"].find({"experimentId": ObjectId(experiment_id)}))
        result = [GPT4AIAgent(experiment_id, agent["name"], agent["instructions"]) for agent in result]
        return result


if __name__ == "__main__":
    db = DBProxy()
    print(db.get_ai_agents("67d5f72320477ecc5f9768d5"))
    #db.insert_event_batch([Event("Test Event", 1), Event("Another Test Event", 2)])