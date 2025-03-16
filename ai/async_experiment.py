import asyncio
from typing import List, Optional, Callable, cast

import openai as openai

from models.gpt_agent import GPT4AIAgent
from ai.user import User
from ai.ai_agent import AIAgent
from ai.event import Event
from ai.experiment import Experiment


class AsyncExperiment(Experiment):
    def __init__(self,
                 id: str,
                 name: str,
                 ai_agents: List[AIAgent],
                 max_length: int,
                 ):
        super().__init__(id, name, ai_agents, max_length)

    async def perform(self):
        old_events: List["Event"] = []
        new_events: List["Event"] = []

        for step in range(self.max_length):
            new_events.clear()

            # Run agents asynchronously in parallel
            await self._foreach_agent(
                self.ai_agents,
                cast(Callable[[AIAgent], None],
                     lambda agent: self._execute_agent(agent, old_events, new_events=new_events)
                     )
            )

            self._send_events_to_db(new_events, step)
            old_events = list(new_events)  # Ensure a copy is made

    async def _foreach_agent(self, agents: List[AIAgent], fn: Callable[[AIAgent], None]) -> None:
        await asyncio.gather(*(fn(ai_agent) for ai_agent in agents))

    async def _execute_agent(self, agent: AIAgent, old_events: List[Event], **kwargs) -> None:
        generated_events: Optional[List[Event]] = agent.react_on_events(old_events)
        kwargs["new_events"].extend(generated_events or [])


if __name__ == "__main__":
    import openai, os
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # 2) Define each persona's instructions
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

    # 3) Create GPT-4 agents with unique instructions
    ai_agents = [
        GPT4AIAgent("123", f"agent{i}", instructions[i])
        for i in range(len(instructions))
    ]

    # 4) Convert each agent to a 'User' (for the user DB)
    users: List[User] = [User(id=agent.id, name=agent.name) for agent in ai_agents]
    user_db: str = "[" + ", ".join([str(user) for user in users]) + "]"

    # 5) Supply the user DB to each agent, then prepare them
    for agent in ai_agents:
        agent.add_user_db(user_db)
        agent.prepare()

    # 6) Create & run the experiment
    experiment = AsyncExperiment(
        id="123",
        name="Test Experiment",
        ai_agents=ai_agents,
        max_length=10,
    )
    asyncio.run(experiment.perform())