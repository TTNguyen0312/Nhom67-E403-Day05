from __future__ import annotations

import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.backend.agent.agent import run_turn

app = FastAPI(title="Vinmec AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store: session_id -> message history list
_sessions: dict[str, list] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/api/agent/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    # Resolve or create session
    session_id = payload.session_id or str(uuid.uuid4())
    history = _sessions.get(session_id, [])

    try:
        updated_history = run_turn(payload.message, history)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    _sessions[session_id] = updated_history
    reply = updated_history[-1].content

    return ChatResponse(reply=reply, session_id=session_id)


@app.delete("/api/agent/chat/{session_id}")
def clear_session(session_id: str):
    """Clear conversation history for a session."""
    _sessions.pop(session_id, None)
    return {"cleared": session_id}
