import time
    
class GeminiAdapter:
    def __init__(self, client):
        self._client = client
        self.models = ModelsNamespace(client)

class ModelsNamespace:
    def __init__(self, client):
        self._client = client

    def generate_content(self, model, contents):
        start = time.time()
        
        response = self._client.models.generate_content(
            model=model,
            contents=contents
        )
        
        latency_ms = (time.time() - start) * 1000
        
        print("model:", model)
        print("latency:", round(latency_ms), "ms")
        print("tokens:", response.usage_metadata.total_token_count)
        
        return response