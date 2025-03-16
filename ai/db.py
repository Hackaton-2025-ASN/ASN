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

    def insert_event_batch(self, events: List[Event], experiment_id: str, time_step: int):
        db = self.client["test"]
        data = []
        for event in events:
            tup = event.to_tuple()
            data.append(
                {
                    "experimentId": ObjectId(experiment_id),
                    "timeStep": time_step,
                    "id": tup[0],
                    "type": tup[1],
                    "userId": ObjectId(tup[2]),
                    "postId": tup[3], # commentId
                    "content": tup[4],
                    "image": None,
                    "followerId": ObjectId(tup[6]),
                    "followeeId": ObjectId(tup[7]),
                }
            )
        result = db.eventstreams.insert_many(data)

    def get_ai_agents(self, experiment_id: str) -> List[AIAgent]:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        db = self.client.get_database("test")

        result = list(db["agents"].find({"experimentId": ObjectId(experiment_id)}))
        result = [GPT4AIAgent(str(agent["_id"]), experiment_id, agent["name"], agent["instructions"]) for agent in result]
        return result


if __name__ == "__main__":
    db = DBProxy()
    print(db.get_ai_agents("67d643216d9dc020b98e57be"))
    #db.insert_event_batch([Event("Test Event", 1), Event("Another Test Event", 2)])