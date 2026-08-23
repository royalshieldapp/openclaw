from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Query
from openai import OpenAI, OpenAIError

app = FastAPI(title="Royal Shield AI API")


NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"


def get_model_config():
    """Get NVIDIA model configuration from environment variables."""
    enable_premium = os.getenv(
        "ENABLE_PREMIUM_MODEL",
        "false"
    ).lower() == "true"

    if enable_premium:
        return os.getenv(
            "AI_PREMIUM_MODEL",
            "meta/llama-3.3-70b-instruct",
        )

    return os.getenv(
        "AI_MODEL",
        "meta/llama-3.1-8b-instruct",
    )


def get_max_tokens():
    """Get max output tokens from environment variable."""
    return int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))


def get_temperature():
    """Get temperature parameter from environment variable."""
    return float(os.getenv("TEMPERATURE", "0.7"))


@app.get("/")
def root() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Royal Shield NVIDIA AI backend active",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ai")
def ai(msg: str = Query(..., min_length=1)) -> dict[str, str]:
    api_key = os.getenv("NVIDIA_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Missing NVIDIA_API_KEY environment variable",
        )

    client = OpenAI(
        api_key=api_key,
        base_url=NVIDIA_BASE_URL,
    )

    model = get_model_config()
    max_tokens = get_max_tokens()
    temperature = get_temperature()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity AI assistant.",
                },
                {
                    "role": "user",
                    "content": msg,
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

    except OpenAIError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"NVIDIA AI request failed: {exc}",
        ) from exc

    output_text = response.choices[0].message.content

    if not output_text:
        raise HTTPException(
            status_code=502,
            detail="NVIDIA returned an empty response",
        )

    return {
        "response": output_text,
        "model": model,
    }
