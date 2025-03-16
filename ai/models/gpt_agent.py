# gpt_agent.py

from typing import Optional, List
from openai import OpenAI
from ai.ai_agent import AIAgent

class GPT4AIAgent(AIAgent):
    """
    A GPT-4o-powered AI agent that integrates OpenAI API completions into the AIAgent framework.
    """
    model_name: str = "gpt-4o"
    context_window: int = 12

    def __init__(
        self,
        id: str,
        experiment_id: str,
        name: str,
        instructions: str,
        image: Optional[bytes] = None
    ):
        super().__init__(id, experiment_id, name, instructions, image)
        self.conversation_history: List[dict] = []
        self.client = OpenAI()  # Initialize OpenAI client; expects OPENAI_API_KEY in env variables

    def _prompt_model(self, prompt: str) -> Optional[str]:
        """
        Sends the prompt to GPT-4o and returns the response.
        """
        return self._generate_response(prompt)

    def _generate_response(
        self,
        prompt: str,
        temperature: float = 0.1,
        top_p: float = 0.05,
        max_tokens: int = 1024
    ) -> str:
        """
        Generates a GPT-4o response by creating a structured conversation consisting
        of a system message (persona instructions) and user message (event strings).
        """

        # Append the new user prompt (event strings) to the history
        self.conversation_history.append({"role": "user", "content": prompt})

        # Structure the conversation with system instructions + history
        messages = [{"role": "system", "content": self.instructions}] + self.conversation_history

        # Trim conversation history if exceeding context window
        if len(messages) > self.context_window:
            messages = [messages[0]] + messages[-self.context_window:]

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,  # 'gpt-4o'
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return ""

        response_text = completion.choices[0].message.content.strip()

        # Store assistant response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response_text})

        return response_text
