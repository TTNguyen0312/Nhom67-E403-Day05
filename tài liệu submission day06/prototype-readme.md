# # Prototype — AI triage Vinmec - Nhóm 67

## MedRoute AI — Prototype Overview

**Mô tả:** Hệ thống agent tự động phân chuyên khoa bệnh nhân dựa trên mô tả triệu chứng tự nhiên.
## 🏷️ Tên Đề Tài
**MedRoute AI - Hệ Thống Agent Tự Động Phân Chuyên Khoa Bệnh Nhân**
> Ứng dụng AI agent phân tuyến bệnh nhân đến đúng chuyên khoa dựa trên mô tả triệu chứng tự nhiên, hỗ trợ giảm tải cho bộ phận tiếp nhận bệnh viện.
 
---
 
## 🛠️ Tech Stack
 
**Frontend**
- React / Next.js - giao diện chat & hiển thị kết quả
- Tailwind CSS - styling 
- Axios - gọi API backend
 
**Backend**
- Python + FastAPI - API server chính
- LangGraph — orchestration agent pipeline
 
**Khác**
- JSON - định dạng trao đổi dữ liệu giữa các tầng
- Git / GitHub - quản lý source code & phối hợp nhóm
- Localhost / ngrok - deploy demo live

## 🔗 Hướng dẫn set up và chạy thử demo
Tạo file .env tại thư mục gốc (root) theo file .env.example
Tạo file .env tại thư mục src/frontend/vinmec-patientguide theo file .env.example
Chạy pip install -r requirements.txt

**Chạy frontend**:
cd .\src\frontend\vinmec-patientguide\
npm i
npm run dev

**Chạy backend**:
Đứng tại thư mục gốc (root)
python -m uvicorn src.backend.main:app --reload

**Khi frontend và backend cùng được khởi chạy thành công thì có thể demo tại http://localhost:5173/?session_id=-001**

## 🔧 Agent Tools
 
Agent sử dụng 4 tools chính, chia thành 2 nhóm: 
 
### Triage tools — `src/backend/agent/tools/triage_tools.py`
 
| Tool | Mô tả |
|---|---|
| `lookup_specialty_info` | Tra cứu thông tin chuyên khoa dựa trên triệu chứng — trả về tên khoa, mức độ ưu tiên, lý do gợi ý |
 
### Booking tools — `src/backend/agent/tools/booking_tools.py`
 
| Tool | Mô tả |
|---|---|
| `look_up_doctors_by_department` | Lấy danh sách bác sĩ theo chuyên khoa đã chọn |
| `look_up_free_schedule` | Lấy các slot lịch khám còn trống của một bác sĩ |
| `book_appointment` | Đặt lịch khám cho bệnh nhân theo slot đã chọn |
 
### Luồng gọi tools
 
```
lookup_specialty_info          ← phân tích triệu chứng → chọn khoa
        ↓
look_up_doctors_by_department  ← lấy DS bác sĩ theo khoa
        ↓
look_up_free_schedule          ← lấy lịch trống của bác sĩ được chọn
        ↓
book_appointment               ← xác nhận đặt lịch
```

## 👥 Phân Công

| Thành viên | Vai trò |
|---|---|
| Tiến | UI/UX, Flow Design, API Design, Agent Tools, Fullstack |
| Quang | LangGraph Agent, System Prompt, Slide |
| Minh | Frontend (React/Next.js) + Backend (FastAPI) |
| Lộc | Backend API, Session Management, Appointment Flow |
| Ngọc | Mock Data, Test Cases, Docs, Slide content |

## 📦 Tech Stack
- **Frontend:** React / Next.js, Tailwind CSS
- **Backend:** Python + FastAPI
- **AI:** LangGraph agent pipeline + Claude API
- **Infra:** localhost / ngrok