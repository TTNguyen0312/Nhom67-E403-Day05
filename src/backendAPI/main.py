from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Vinmec AI Backend")

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running"}

from pydantic import BaseModel
from typing import Optional

class TriageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class TriageResponse(BaseModel):
    reply: str
    next_screen: str
    specialty: Optional[str] = None
    confidence: Optional[float] = None


@app.post("/api/agent/triage", response_model=TriageResponse)
async def triage(payload: TriageRequest):
    msg = payload.message.lower()

    # Mock logic để test frontend
    if "đau ngực" in msg or "khó thở" in msg:
        return TriageResponse(
            reply="Bạn có dấu hiệu nguy hiểm. Vui lòng đến khoa Cấp cứu ngay.",
            next_screen="EmergencyScreen",
            specialty="Cấp cứu",
            confidence=0.98
        )

    if "đau bụng" in msg:
        return TriageResponse(
            reply="Triệu chứng của bạn phù hợp với khoa Tiêu hóa.",
            next_screen="SpecialtyScreen",
            specialty="Tiêu hóa",
            confidence=0.88
        )

    return TriageResponse(
        reply="Mình chưa đủ chắc chắn. Mình sẽ chuyển bạn sang nhân viên hỗ trợ.",
        next_screen="EscalateScreen",
        specialty=None,
        confidence=0.45
    )