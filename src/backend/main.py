from __future__ import annotations

import json
import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.backend.agent.agent import run_turn
from src.backend.agent.tools.booking_tools import (
    DEPARTMENTS,
    DOCTORS,
    book_appointment,
    look_up_free_schedule,
)

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
    image: Optional[str] = None  # base64-encoded image (no data URI prefix)


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
        updated_history = run_turn(payload.message, history, image_b64=payload.image or None)
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


# ── Booking REST endpoints ────────────────────────────────────────────────────


@app.get("/api/departments/{dept_id}/doctors")
def get_doctors_by_department(dept_id: str):
    """Return available doctors for a department."""
    dept = next((d for d in DEPARTMENTS if d["id"] == dept_id), None)
    if dept is None:
        raise HTTPException(status_code=404, detail=f"Khoa '{dept_id}' không tồn tại.")
    doctors = [
        {
            "id": d["id"],
            "name": d["name"],
            "title": d.get("title", ""),
            "avatar": d.get("avatar", "👨‍⚕️"),
            "experience": d.get("experience", 0),
            "rating": d.get("rating", 0),
            "reviewCount": d.get("reviewCount", 0),
            "consultationFee": d.get("consultationFee", 0),
            "subSpecialties": d.get("subSpecialties", []),
        }
        for d in DOCTORS
        if d["departmentId"] == dept_id and d.get("isAvailable")
    ]
    return {"department": {"id": dept["id"], "name": dept["name"], "icon": dept.get("icon", "")}, "doctors": doctors}


@app.get("/api/doctors/{doctor_id}/schedule")
def get_doctor_schedule(doctor_id: str, date: str):
    """Return available time slots for a doctor on a given date."""
    result_json = look_up_free_schedule.invoke({"doctor_id": doctor_id, "date": date})
    result = json.loads(result_json)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


class BookingRequest(BaseModel):
    date: str
    time: str
    department_id: str
    doctor_id: str


@app.post("/api/booking")
def create_booking(payload: BookingRequest):
    """Create a confirmed booking."""
    result_json = book_appointment.invoke({
        "date": payload.date,
        "time": payload.time,
        "department_id": payload.department_id,
        "doctor_id": payload.doctor_id,
    })
    result = json.loads(result_json)
    if "error" in result:
        raise HTTPException(status_code=409, detail=result["error"])
    return result
