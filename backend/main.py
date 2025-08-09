from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_core import get_ai_response

# Pydantic model for the request body
class Message(BaseModel):
    text: str

app = FastAPI()

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ADD THIS ROOT ENDPOINT BACK ---
@app.get("/")
def read_root():
    """
    This endpoint provides a simple confirmation that the backend is running.
    """
    return {"message": "JustAssist Backend is running!"}
# -----------------------------------

@app.post("/chat")
async def handle_chat(message: Message):
    """
    This endpoint receives a user's message, gets a response from the AI,
    and sends it back to the frontend.
    """
    response = get_ai_response(message.text)
    return {"response": response}