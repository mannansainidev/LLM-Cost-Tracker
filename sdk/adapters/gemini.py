import time
from sdk.logger import log_event

PRICING = {
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40,  "input_long": 0.10,  "output_long": 0.40},
    "gemini-2.5-flash":      {"input": 0.30, "output": 2.50,  "input_long": 0.30,  "output_long": 2.50},
    "gemini-2.5-pro":        {"input": 1.25, "output": 10.00, "input_long": 2.50,  "output_long": 15.00},
    "gemini-3-flash":        {"input": 0.50, "output": 3.00,  "input_long": 0.50,  "output_long": 3.00},
    "gemini-3.1-pro":        {"input": 2.00, "output": 12.00, "input_long": 4.00,  "output_long": 18.00},
}

class GeminiAdapter:
    def __init__(self, client):
        self._client = client
        self.models = ModelsNamespace(client)

class ModelsNamespace:
    def __init__(self, client):
        self._client = client

    def generate_content(self, model="unknown", contents=None):
        start = time.time()
        response = self._client.models.generate_content(
            model=model,
            contents=contents
        )
        latency_ms = (time.time() - start) * 1000

        input_tokens  = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count

        prices = PRICING.get(model, {"input": 0, "output": 0, "input_long": 0, "output_long": 0})
        tier   = "input_long" if input_tokens > 200_000 else "input"
        cost   = (
            (input_tokens  / 1_000_000) * prices[tier] +
            (output_tokens / 1_000_000) * prices[tier.replace("input", "output")]
        )

        log_event(
            model=model,
            provider="gemini",      
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            latency_ms=latency_ms,
            cost=cost,
        )

        return response