from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Query
from openai import OpenAI

app = FastAPI(title="OpenClaw API")


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
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="You are a cybersecurity AI assistant.",
        input=msg,
    )
    return {"response": response.output_text}
