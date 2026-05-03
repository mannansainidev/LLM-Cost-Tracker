import json
from pathlib import Path

QUEUE_FILE = Path("queue.jsonl")

def push(event: dict):
    with QUEUE_FILE.open("a") as f:
        f.write(json.dumps(event) + "\n")