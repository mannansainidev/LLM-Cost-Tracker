from flask import Flask, request
from wrapper import *
import anthropic
import os
import google.generativeai as genai
from openai import OpenAI

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY")
CHATGPT_API_KEY    = os.getenv("CHATGPT_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return {"error": 404, "reason": "Invalid route, use /api/{provider}"}, 404

@app.route("/api/claude", methods=["POST"])
def claude():
    data = request.json
    client = ClaudeAdapter(anthropic.Anthropic(api_key=ANTHROPIC_API_KEY))
    response = client.messages.create(
        model=data.get("model", "claude-sonnet-4-6"),
        max_tokens=data.get("max_tokens", 1024),
        messages=data["messages"]
    )
    return {"content": response.content[0].text}

@app.route("/api/gemini", methods=["POST"])
def gemini():
    data = request.json
    client = GeminiAdapter(genai.Client(api_key=GEMINI_API_KEY))
    response = client.models.generate_content(
        model=data.get("model", "gemini-2.5-flash"),
        contents=data["contents"]
    )
    return {"content": response.text}

@app.route("/api/chatgpt", methods=["POST"])
def chatgpt():
    data = request.json
    client = OpenAIAdapter(OpenAI(api_key=CHATGPT_API_KEY))
    response = client.chat.completions.create(
        model=data.get("model", "gpt-4o"),
        messages=data["messages"]
    )
    return {"content": response.choices[0].message.content}

if __name__ == "__main__":
    missing = [k for k in ["ANTHROPIC_API_KEY", "GEMINI_API_KEY", "CHATGPT_API_KEY"] if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"Missing env vars: {missing}")
    app.run(debug=True)