# main.py

import os
import asyncio
from fastapi import FastAPI, BackgroundTasks, Query
import uvicorn
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

from ai.db import DBProxy
from ai.experiment import Experiment
from ai.user import User

app = FastAPI()

@app.get("/ai/experiment/start")
async def start_experiment(
    experiment_id: str = Query(..., alias="experiment-id", description="Unique experiment identifier"),
    duration: int = Query(..., description="Number of steps to run the experiment"),
    background_tasks: BackgroundTasks = None
):
    async def run_experiment():
        await asyncio.sleep(1)
        
        db_proxy = DBProxy()
        ai_agents = db_proxy.get_ai_agents(experiment_id)
        print(f"Retrieved {len(ai_agents)} agents for experiment {experiment_id}")
        
        users = [User(name=agent.name, id=agent.id) for agent in ai_agents]
        user_db = "[" + ", ".join(str(user) for user in users) + "]"
        for agent in ai_agents:
            agent.add_user_db(user_db)
            agent.prepare()
        
        experiment = Experiment(
            id=experiment_id,
            name="Experiment from DB",
            ai_agents=ai_agents,
            max_length=duration,
        )
        experiment.perform()
    
    background_tasks.add_task(run_experiment)
    return {"status": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

