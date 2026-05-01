import time

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

        latency_ms = (time.time() - start) * 1000

        print("model:", kwargs.get("model"))
        print("latency:", round(latency_ms), "ms")
        print("input tokens:", response.usage.input_tokens)    
        print("output tokens:", response.usage.output_tokens)  

        return response