import requests

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


class LlamaAIAgent(AIAgent):
    def __init__(self, name: str, instructions: str, image: Optional[bytes] = None):
        """
        Initializes the AI agent with a name, persona instructions, and optional profile image.
        """
        super().__init__(name, instructions, image)
        self.model_name = "llama2-uncensored:7b-chat"

    def _build_agent_prompt(self, social_media_context: str) -> str:

        prompt = f"""
    [System]
    You are {self.name}. Here is your personality:
    {self.instructions}

    This is a **social media platform** where users:
    - Create **posts**
    - **Like, comment, and reply** to posts
    - **Follow** other users

    Your job is to **analyze the feed** and decide how to engage.
    - You can **comment, like, or reply to posts**.
    - Your responses must be **natural, concise, and engaging**.
    - If a post is popular (many likes), **acknowledge its popularity**.
    - If a post is controversial, **offer a thoughtful or humorous take**.

    **Social Media Feed:**
    {social_media_context}

    **Your Response Rules:**
    - Choose one action: **comment, reply, or like**.
    - If you **comment or reply**, write a **short, relevant response**.
    - If you **like** something, say why it interests you.
    - DO NOT include disclaimers or out-of-character remarks.

    **Example Interactions:**
    - Post: "What’s your favorite sci-fi book?"  
    AI: "I love sci-fi! Dune is a masterpiece."
    - Post: "Morning coffee or tea?"  
    AI: "Coffee all the way ☕!"
    - Post: "This movie was overrated."  
    AI: "I think it had some great moments, but I get why some didn’t like it."

    Now, based on the feed, **decide what to do and generate a response**.
        """.strip()

        # ✅ SEND PROMPT TO OLLAMA
        response = _generate_response(prompt, chat_mode=True)

        return response  # Return the model-generated response
