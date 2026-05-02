import os

from fastapi import FastAPI, HTTPException
from openai import APIStatusError, OpenAI

app = FastAPI(title="Royal Shield API", version="1.0.0")

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
MODEL_CANDIDATES = [
    model.strip()
    for model in os.getenv("OPENAI_MODELS", DEFAULT_MODEL).split(",")
    if model.strip()
]


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured on the server.",
        )
    return OpenAI(api_key=api_key)


@app.get("/")
def root():
    return {
        "status": "ok",
        "app": "Royal Shield",
        "message": "Royal Shield backend active 🔐",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "service": "railway"}


@app.get("/ai")
def ai(msg: str):
    client = get_openai_client()
    last_error = None

    for model in MODEL_CANDIDATES:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity AI assistant."},
                    {"role": "user", "content": msg},
                ],
            )
            content = response.choices[0].message.content
            return {"response": content}
        except APIStatusError as exc:
            last_error = exc
            # Try next model if this one is not available for the project.
            if exc.status_code == 403 and "model" in str(exc).lower():
                continue
            if exc.status_code == 401:
                raise HTTPException(
                    status_code=502,
                    detail="OpenAI authentication failed. Verify OPENAI_API_KEY.",
                ) from exc
            raise HTTPException(status_code=502, detail="OpenAI API request failed.") from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc

    attempted = ", ".join(MODEL_CANDIDATES)
    raise HTTPException(
        status_code=502,
        detail=(
            "No configured model is accessible for this project. "
            f"Tried: {attempted}. Set OPENAI_MODELS/OPENAI_MODEL to allowed models."
        ),
    ) from last_error
