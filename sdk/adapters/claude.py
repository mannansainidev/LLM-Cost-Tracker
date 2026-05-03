import time
from sdk.logger import log_event

PRICING = {
    "claude-haiku-4-5":   {"input": 1.00,  "output": 5.00},
    "claude-sonnet-4-6":  {"input": 3.00,  "output": 15.00},
    "claude-opus-4-6":    {"input": 5.00,  "output": 25.00},
    "claude-opus-4-7":    {"input": 5.00,  "output": 25.00},
}

class ClaudeAdapter:
    def __init__(self, client):
        self._client = client
        self.messages = MessagesNamespace(client)  

class MessagesNamespace:
    def __init__(self, client):
        self._client = client

    def create(self, **kwargs):                    
        start = time.time()

        response = self._client.messages.create(
            **kwargs  
        )
        model = kwargs.get("model")
        latency_ms = (time.time() - start) * 1000
        prices = PRICING.get(model, {"input": 0, "output": 0})
        cost = (
            (response.usage.input_tokens  / 1_000_000) * prices["input"] +
            (response.usage.output_tokens / 1_000_000) * prices["output"]
        )
        
        log_event(
            model=model,
            provider="claude",      
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            latency_ms=latency_ms,
            cost=cost,
        )
        return response