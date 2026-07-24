import os

from dotenv import load_dotenv
from groq import Groq
load_dotenv()
MODEL = "llama-3.1-8b-instant"
_client = Groq | None = None 

def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("no api key set")
        _client = Groq(api_key=api_key)
    return _client

def chat(messages: list[dict], tools: list[dict] | None = None) -> object:
    client = get_client()
    kwargs = {"model": MODEL, "messages": messages}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    return client.chat.completion.create(**kwargs)
