from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass

from chatbot import ChatAgent  
from model import ChatRequest, ChatRequestModel 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




chat_agent = ChatAgent()  

@app.post("/chat")
async def chat_endpoint(request: ChatRequestModel):
    # Convert Pydantic model to ChatRequest dataclass
    chat_request = ChatRequest(session_id=request.session_id, message=request.message)
    response = chat_agent.chat(chat_request)
    return {"response": response}