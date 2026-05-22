from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Query
from openai import OpenAI
from openai import OpenAIError

app = FastAPI(title="OpenClaw API")

# Load AI configuration from environment variables
def get_model_config():
    """Get AI model configuration from environment variables."""
    enable_premium = os.getenv("ENABLE_PREMIUM_MODEL", "false").lower() == "true"
    
    if enable_premium:
        return os.getenv("AI_PREMIUM_MODEL", "gpt-4-turbo")
    else:
        return os.getenv("AI_MODEL", "gpt-4o-mini")

def get_max_tokens():
    """Get max output tokens from environment variable."""
    return int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))

def get_temperature():
    """Get temperature parameter from environment variable."""
    return float(os.getenv("TEMPERATURE", "0.7"))


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "message": "OpenClaw backend active"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ai")
def ai(msg: str = Query(..., min_length=1)) -> dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Missing OPENAI_API_KEY environment variable",
        )

    client = OpenAI(api_key=api_key)
    model = get_model_config()
    max_tokens = get_max_tokens()
    temperature = get_temperature()
    
    try:
        response = client.responses.create(
            model=model,
            instructions="You are a cybersecurity AI assistant.",
            input=msg,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    except OpenAIError as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc

    output_text = response.output_text
    if not output_text:
        raise HTTPException(status_code=502, detail="OpenAI returned an empty response")

    return {"response": output_text}
