from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()

# Tell FastAPI where HTML files are
templates = Jinja2Templates(directory="templates")

# Request body model
class ChatRequest(BaseModel):
    message: str

# Load UI
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# Chat API
@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message.lower()

    if "hello" in user_message:
        reply = "Hello! How can I help you?"
    elif "java" in user_message:
        reply = "Java is a powerful backend language."
    elif "bye" in user_message:
        reply = "Goodbye! Have a great day 😊"
    else:
        reply = "Sorry, I didn't understand that."

    return {"response": reply}
