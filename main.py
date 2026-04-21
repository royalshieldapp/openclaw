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
