from fastapi import FastAPI
from openai import OpenAI

app = FastAPI(
    title="Royal Shield API",
    version="1.0.0"
)
client = OpenAI()

@app.get("/")
def root():
    return {
        "status": "ok",
        "app": "Royal Shield",
        "message": "Royal Shield backend active 🔐"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "railway"
    }

@app.get("/ai")
def ai(msg: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a cybersecurity AI assistant."},
            {"role": "user", "content": msg}
        ]
    )
    return {"response": response.choices[0].message.content}
