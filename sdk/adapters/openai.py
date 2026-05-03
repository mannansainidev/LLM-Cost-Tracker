import time
from sdk.logger import log_event

# cost per 1M tokens (update as pricing changes)
PRICING = {
    "gpt-4o":            {"input": 5.00,  "output": 15.00},
    "gpt-4o-mini":       {"input": 0.15,  "output": 0.60},
    "gpt-3.5-turbo":     {"input": 0.50,  "output": 1.50},
}

class OpenAIAdapter:
    def __init__(self, client):
        self._client = client
        self.chat = ChatNamespace(client)

class ChatNamespace:
    def __init__(self, client):
        self._client = client
        self.completions = CompletionsNamespace(client)

class CompletionsNamespace:
    def __init__(self, client):
        self._client = client

    def create(self, **kwargs):
        start = time.time()

        response = self._client.chat.completions.create(**kwargs)
        
        latency_ms = (time.time() - start) * 1000

        usage = response.usage
        model = kwargs.get("model", "unknown")
        prices = PRICING.get(model, {"input": 0, "output": 0})
        
        cost = (
            (usage.prompt_tokens / 1_000_000) * prices["input"] +
            (usage.completion_tokens / 1_000_000) * prices["output"]
        )
        
        # build the event log
        log_event(
            model=model,
            provider="openai",      
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            latency_ms=latency_ms,
            cost=cost,
        )
        
        return response  # original response untouched