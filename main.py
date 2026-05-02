import os

from fastapi import FastAPI, HTTPException
from openai import APIStatusError, OpenAI

app = FastAPI(title="Royal Shield API", version="1.0.0")

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


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
    try:
        response = get_openai_client().chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a cybersecurity AI assistant."},
                {"role": "user", "content": msg},
            ],
        )
    except HTTPException:
        raise
    except APIStatusError as exc:
        # Convert provider errors to controlled HTTP responses.
        detail = f"OpenAI API error ({exc.status_code}): {exc.response.text}"
        raise HTTPException(status_code=exc.status_code or 502, detail=detail) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc

    content = response.choices[0].message.content
    return {"response": content, "model": DEFAULT_MODEL}
