import json
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("events.jsonl")

def log_event(model, provider, input_tokens, output_tokens, latency_ms, cost):
    event = {
        "timestamp":     datetime.now(timezone.utc).isoformat(),
        "provider":      provider,
        "model":         model,
        "input_tokens":  input_tokens,
        "output_tokens": output_tokens,
        "latency_ms":    round(latency_ms, 2),
        "cost_usd":      round(cost, 6),
    }
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(event) + "\n")