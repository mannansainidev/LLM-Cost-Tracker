import time
from sdk.adapters.openai import OpenAIAdapter
from sdk.adapters.gemini import GeminiAdapter
from sdk.adapters.claude import ClaudeAdapter

def wrap(client):
    provider = detect_provider(client)
    
    if provider == "openai":
        return OpenAIAdapter(client)
    if provider == "gemini":
        return GeminiAdapter(client)
    if provider == "claude":
        return ClaudeAdapter
    
    raise ValueError(f"Unsupported client: {type(client)}")

def detect_provider(client):
    module = type(client).__module__
    if "openai" in module:
        return "openai"
    if "anthropic" in module:
        return "claude"
    if "google" in module:
        return "gemini"