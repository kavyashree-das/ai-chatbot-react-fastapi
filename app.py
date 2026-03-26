from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pydantic import BaseModel
from groq import Groq

import os
from dotenv import load_dotenv
from pathlib import Path
from dotenv import load_dotenv


## Force load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Create OpenAI client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str




chat_history = []

@app.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message

    try:
        chat_history.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=chat_history
        )

        ai_reply = response.choices[0].message.content

        chat_history.append({"role": "assistant", "content": "You are a helpful assistant.Give short, well-formatted answers using bullet points."})

        return {"response": ai_reply}

    except Exception as e:
        print("ERROR:", e)
        return {"response": "AI is not responding. Please try again later."}
