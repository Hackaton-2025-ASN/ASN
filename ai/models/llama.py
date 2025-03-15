from typing import Optional

import requests

from ai.ai_agent import AIAgent


class LlamaAIAgent(AIAgent):
    model_name: str = "llama2-uncensored:7b-chat"
    context_window: int = 12

    def __init__(self, experiment_id: str, name: str, instructions: str, image: Optional[bytes] = None):
        """
        Initializes the AI agent with a name, persona instructions, and optional profile image.
        """
        super().__init__(experiment_id, name, instructions, image)

        self.conversation_history = []

    def _prompt_model(self, prompt: str) -> Optional[str]:
        response = self._generate_response(prompt)
        return response if response else None
    
    def _generate_response(self,
                    prompt: str,
                    temperature: float = 0.0,
                    top_p: float = 0.0,
                    max_tokens: int = 8192,
                    chat_mode: bool = True
                            ) -> str:
        """
        Sends a prompt to the running Ollama server and returns the generated text.
        
        - `chat_mode=True` → Uses `/api/chat` for multi-turn chat.
        - `chat_mode=False` → Uses `/api/generate` for single text completion.
        """
        url = "http://localhost:11434/api/chat" if chat_mode else "http://localhost:11434/api/generate"

        request_body = {
            "model": self.model_name,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": False
        }

        self.conversation_history.append({'role': 'user', 'content': prompt})

        if len(self.conversation_history) > self.context_window:
            self.conversation_history = self.conversation_history[:2] + \
                                        self.conversation_history[-self.context_window + 2:]
        else:
            self.conversation_history = self.conversation_history[-self.context_window:]

        if chat_mode:
            request_body["messages"] = self.conversation_history
        else:
            request_body["prompt"] = prompt

        response = requests.post(url, json=request_body)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return ""

        data = response.json()
        return data.get("response", data.get("message", {}).get("content", "")).strip()