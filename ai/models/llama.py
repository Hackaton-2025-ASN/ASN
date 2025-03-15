import requests

from ai.ai_agent import AIAgent
class LlamaAIAgent(AIAgent):
    def __init__(self, name: str, instructions: str, image: Optional[bytes] = None):
        """
        Initializes the AI agent with a name, persona instructions, and optional profile image.
        """
        super().__init__(name, instructions, image)
        self.model_name = "llama2-uncensored:7b-chat-" + self.id +"-"+ self.name

        # ✅ SEND PROMPT TO OLLAMA
    def _prompt_model(self, prompt: str) -> Optional[str]:
        response = _generate_response(prompt, chat_mode=True)

        return response  # Return the model-generated response
    
    def _generate_response(prompt: str,
                             model_name="llama2-uncensored:7b-chat",
                             temperature=0.7,
                             top_p=0.9,
                             max_tokens=256,
                             chat_mode=False):
        """
        Sends a prompt to the running Ollama server and returns the generated text.
        
        - `chat_mode=True` → Uses `/api/chat` for multi-turn chat.
        - `chat_mode=False` → Uses `/api/generate` for single text completion.
        """
        url = "http://localhost:11434/api/chat" if chat_mode else "http://localhost:11434/api/generate"

        payload = {
            "model": model_name,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": False
        }

        if chat_mode:
            payload["messages"] = [{"role": "user", "content": prompt}]
        else:
            payload["prompt"] = prompt

        response = requests.post(url, json=payload)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return ""

        data = response.json()
        return data.get("response", data.get("message", {}).get("content", "")).strip()