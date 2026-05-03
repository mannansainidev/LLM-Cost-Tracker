import json
from pathlib import Path
from collections import defaultdict

QUEUE_FILE = Path("queue.jsonl")

def consume():
    if not QUEUE_FILE.exists():
        print("No events in queue.")
        return

    totals = defaultdict(lambda: {"calls": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0})

    with QUEUE_FILE.open("r") as f:
        for line in f:
            event = json.loads(line)
            key = f"{event['provider']}/{event['model']}"
            totals[key]["calls"]         += 1
            totals[key]["input_tokens"]  += event["input_tokens"]
            totals[key]["output_tokens"] += event["output_tokens"]
            totals[key]["cost_usd"]      += event["cost_usd"]

    print(f"{'Model':<30} {'Calls':>6} {'Input':>10} {'Output':>10} {'Cost':>10}")
    print("-" * 70)
    for model, data in totals.items():
        print(f"{model:<30} {data['calls']:>6} {data['input_tokens']:>10} {data['output_tokens']:>10} ${data['cost_usd']:>9.4f}")