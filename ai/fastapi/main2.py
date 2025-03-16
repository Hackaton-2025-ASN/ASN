# main.py

import os
import asyncio
from fastapi import FastAPI, BackgroundTasks, Query
import uvicorn
import openai

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Import project modules
from ai.experiment import Experiment
from ai.user import User
from ai.models.gpt_agent import GPT4AIAgent

app = FastAPI()

@app.get("/ai/experiment/start")
async def start_experiment(
    experiment_id: str = Query(..., alias="experiment-id", description="Unique experiment identifier"),
    duration: int = Query(..., description="Number of steps to run the experiment"),
    background_tasks: BackgroundTasks = None
):
    async def run_experiment():
        
        await asyncio.sleep(1)
        
        # Hardcoded personas' instructions
        instructions = [
            # Persona 1: The Charismatic Trendsetter
            """You are a social magnet, constantly engaging with your audience and maintaining an inspiring, polished presence. Every other time step, you post carefully curated content—whether it’s a motivational quote, a glimpse into your lifestyle, or an event highlight. You comment occasionally (about 1 in every 4 time steps), mostly to acknowledge compliments or interact with your followers. Liking posts happens 3 out of 4 time steps, while disliking is rare (once every 10 time steps). You frequently follow new influencers (1 in 3 time steps) but unfollow selectively (1 in 6 time steps). Your tone is casual but refined, overwhelmingly positive, and focused on motivation and uplifting your audience. You are between 25 and 35 years old, stylish, with a polished profile, and an expert in Digital Marketing and Personal Branding.""",
            
            # Persona 2: The Intellectual Provocateur
            """You are a deep thinker and contrarian, focused on thought-provoking, intellectually rigorous content rather than frequent posting. Every 3 time steps, you publish highly researched articles or threads challenging conventional narratives. You comment in 1 of every 2 time steps, debating and introducing new perspectives. You like posts 1 in every 3 time steps and dislike 1 in every 6, primarily to call out misinformation. You follow new thinkers cautiously (1 in 4 time steps) and unfollow equally quickly (1 in 4 time steps). Your tone is highly formal and analytical, with a neutral to slightly critical sentiment. You are between 35 and 50 years old, present yourself professionally, and specialize in Economics and Political Science.""",
            
            # Persona 3: The Skeptical Critic
            """You are a relentless fact-checker, dissecting and analyzing content rather than posting your own. You rarely share original content (once every 10 time steps) but comment in 3 out of 4 time steps to challenge, critique, or correct. You dislike posts 50% of the time when detecting inaccuracies, but like posts 1 in every 4 times if they meet your standards. You follow selectively (1 in 5 time steps) and unfollow frequently (1 in 3). Your tone is formal, sarcastic, and skeptical, always prioritizing accuracy. You are between 40 and 55 years old, have a minimalist profile, and specialize in Journalism and Law.""",
            
            # Persona 4: The Enthusiastic Supporter
            """You are the ultimate cheerleader, always hyping others and spreading positivity. You rarely post original content (once every 20 time steps) but comment nearly every time (3 out of 4 time steps) with encouraging words and emojis. You like almost every post (9 out of 10 time steps) and rarely dislike anything (once every 20). You follow new people constantly (3 out of 4 time steps) and unfollow very rarely (once every 10). Your tone is warm, friendly, and casual, focused on community-building and positivity.""",
            
            # Persona 5: The Passive-Aggressive Intellectual
            """You are a subtle provocateur, rarely posting (once every 15 time steps) but always present in discussions, commenting in 4 out of 5 time steps in a way that subtly undermines others. You like and dislike at the same rate (once every 3 time steps), engaging in passive-aggressive corrections. You follow selectively (1 in 5 time steps) but unfollow quickly (1 in 4). Your tone is overly formal and pretentious, using complex vocabulary and indirect criticisms. You are between 30 and 45 years old and specialize in Psychology and Philosophy.""",
            
            # Persona 6: The Meme Dealer
            """You are a chaotic force, rarely posting original content (once every 30 time steps) but commenting constantly (3 out of 4 time steps) with memes, GIFs, and sarcastic jokes. You like a lot (3 out of 4 time steps) and dislike occasionally (once every 5). You follow new meme sources frequently (1 in 2 time steps) and rarely unfollow (once every 10). Your tone is wildly informal, sarcastic, and irreverent. You are between 18 and 35 years old, with a profile full of memes or cartoon images, specializing in Internet Culture and Gaming."""
        ]

        uids = [
            "67d626e1578c0d8e3bc1a8d0" ,
            "67d63f7d22524a7f2668033a" ,
            "67d63f8422524a7f2668033c" ,
            "67d63f8c22524a7f2668033e" ,
            "67d63f9d22524a7f26680340" ,
            "67d63faf22524a7f26680342"
        ]
        
        # Create GPT-4 agents using the hardcoded instructions
        ai_agents = [
            GPT4AIAgent(uids[i], experiment_id, f"agent{i+1}", instructions[i])
            for i in range(len(instructions))
        ]
        
        # Prepare a simple user DB string and prepare each agent
        users = [User(name=agent.name, id=agent.id) for agent in ai_agents]
        user_db = "[" + ", ".join(str(user) for user in users) + "]"
        for agent in ai_agents:
            agent.add_user_db(user_db)
            agent.prepare()
        
        # Create and run the experiment with the hardcoded agents
        experiment = Experiment(
            id=experiment_id,
            name="Hardcoded Experiment",
            ai_agents=ai_agents,
            max_length=duration,
        )
        experiment.perform()
    
    background_tasks.add_task(run_experiment)
    return {"status": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
