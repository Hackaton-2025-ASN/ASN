import requests

# 1) Define a helper function to query Ollama:
def generate_response_ollama(prompt,
                             model_name="llama2-uncensored:7b-chat",
                             temperature=0.7,
                             top_p=0.9,
                             max_tokens=256,
                             chat_mode=False):
    """
    Sends a prompt to the running Ollama server and returns the generated text.
    - If `chat_mode=True`, uses the chat API (`/api/chat`).
    - Otherwise, uses the normal text generation API (`/api/generate`).
    """
    url = "http://localhost:11434/api/chat" if chat_mode else "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stream": False  # Get full response at once
    }

    if chat_mode:
        # Chat-based API (must send messages array)
        payload["messages"] = [{"role": "user", "content": prompt}]
    else:
        # Simple text generation API (must send prompt)
        payload["prompt"] = prompt

    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return ""

    data = response.json()
    return data.get("response", data.get("message", {}).get("content", "")).strip()  # Adjust for both APIs


# 2) Define the forum posts we want to show them:
forum_posts = [
    {"author": "System", "content": "Welcome to the discussion! Share your thoughts on your favorite movie."},
    {"author": "User1",  "content": "I absolutely love 'The Matrix'. The themes are so deep!"},
    {"author": "User2",  "content": "My favorite is 'Inception'. It's mind-bending and visually stunning."}
]

# 3) Convert forum_posts into a simple text snippet for the prompt:
def build_forum_text(posts):
    return "\n".join(f"{post['author']}: {post['content']}" for post in posts)

forum_text = build_forum_text(forum_posts)

# 4) Define two personas: Alice (20-year-old blonde woman), Bob (30-year-old Asian man).
agents = [
    {
        "name": "Alice",
        "persona": "You are Alice, a 20-year-old blonde woman who is friendly and upbeat. You enjoy casual conversations and pop culture references."
    },
    {
        "name": "Bob",
        "persona": "You are Bob, a 30-year-old Asian man who is thoughtful and likes to offer insights. You're interested in tech and detailed analyses."
    }
]

# 5) Prompt template: we feed the persona + forum context + instructions
def build_agent_prompt(agent_name, agent_persona, forum_text):
    return f"""
[System]
You will respond as {agent_name}. The details of your persona:
{agent_persona}

Below is the current discussion:
{forum_text}

Please reply to the above discussion in character as {agent_name}, referencing the forum posts if needed.
Keep it short, friendly, and natural. Do not include extra disclaimers. Do not say anything else besides your response and what you respond to.
For example, Post: "I agree",  
    """.strip()

# 6) Main logic: simply prompt each agent, see their response
if __name__ == "__main__":
    # Test direct query
    test_prompt = "Hello, how are you?"
    print("Test prompt output:", generate_response_ollama(test_prompt, chat_mode=False))

    # Test each agent in the discussion
    for agent in agents:
        prompt = build_agent_prompt(agent["name"], agent["persona"], forum_text)
        print(f"\n--- Prompting {agent['name']} ---")
        print("PROMPT:\n", prompt)
        response = generate_response_ollama(prompt, chat_mode=True)
        print(f"\n{agent['name']} says:\n{response}\n{'-'*50}")
